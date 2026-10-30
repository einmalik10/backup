"""Alle Bilder für die Pitch-Mappen: heute (PC/Handy) und neu (PC, Handy-Start, komplette Handy-Seite).

Aufruf:
    python shots.py --kunden kunden.py --demo-base http://localhost:8765/showcase/ --out img [slug ...]

Voraussetzungen:
- Die Demo-Seiten laufen über einen lokalen Server, z. B.  python -m http.server 8765  im Demo-Ordner
  (im Hintergrund starten). Demo-URL = demo-base + <slug>.html
- Kundendatei mit KUNDEN = [ {...}, ... ] (Schema: assets/kunden_beispiel.py)
- vorher_art "website": die echte Seite (vorher_url) wird fotografiert
  vorher_art "suche":   assets/vorher.html wird mit k["suche"] befüllt (nachgestellte Suchansicht)
  vorher_art "fehler":  assets/fehlerseite.html mit k["fehler"] = {"domain", optional "text", "code"}
                        (Domain löst nicht auf / Server tot → kein echter Screenshot möglich)

Erzeugt pro slug:
  <slug>-alt-pc.png, <slug>-alt-handy.png, <slug>-neu-pc.png, <slug>-neu-handy-1.png,
  <slug>-neu-handy-s1..sN.png (komplette Handy-Seite, Bildschirm für Bildschirm)
"""
import argparse
import importlib.util
import json
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

HIER = Path(__file__).resolve().parent
# Normale Chrome-Kennung: viele Hoster (z. B. IONOS) antworten "HeadlessChrome" mit 503/403, das wäre ein falscher Befund
DESKTOP = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"


def lade_kunden(pfad):
    spec = importlib.util.spec_from_file_location("kunden", pfad)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.KUNDEN


def shot(page, url, ziel, warten=900):
    page.goto(url, wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(warten)
    page.screenshot(path=str(ziel))


def segmente(page, url, out, slug, max_n=8):
    for alt in out.glob(f"{slug}-neu-handy-s*.png"):
        alt.unlink()
    page.goto(url, wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(900)
    hoehe = page.evaluate("document.documentElement.scrollHeight")
    schritt = 844 - 24
    n = min(max_n, -(-(hoehe - 24) // schritt))
    for i in range(n):
        page.evaluate("y => window.scrollTo(0, y)", min(i * schritt, max(0, hoehe - 844)))
        page.wait_for_timeout(350)
        page.screenshot(path=str(out / f"{slug}-neu-handy-s{i + 1}.png"))
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--kunden", required=True)
    ap.add_argument("--demo-base", required=True)
    ap.add_argument("--out", default="img")
    ap.add_argument("--vorher-vorlage", default=str(HIER.parent / "assets" / "vorher.html"))
    ap.add_argument("slugs", nargs="*")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    vorher = Path(a.vorher_vorlage).resolve().as_uri()
    fehler = (HIER.parent / "assets" / "fehlerseite.html").resolve().as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pc = b.new_context(viewport={"width": 1440, "height": 900}, locale="de-DE", reduced_motion="reduce", user_agent=DESKTOP).new_page()
        ha = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
                           locale="de-DE", reduced_motion="reduce", user_agent=IPHONE).new_page()
        for k in lade_kunden(a.kunden):
            s = k["slug"]
            if a.slugs and s not in a.slugs:
                continue
            demo = a.demo_base.rstrip("/") + f"/{s}.html"
            shot(pc, demo, out / f"{s}-neu-pc.png")
            shot(ha, demo, out / f"{s}-neu-handy-1.png")
            n = segmente(ha, demo, out, s)
            if k["vorher_art"] == "website":
                for page, name in ((pc, "pc"), (ha, "handy")):
                    try:
                        page.goto(k["vorher_url"], wait_until="load", timeout=30000); page.wait_for_timeout(2200)
                        page.screenshot(path=str(out / f"{s}-alt-{name}.png"))
                    except Exception as e:
                        print(f"   ! {s} alt {name}: {type(e).__name__}")
            elif k["vorher_art"] == "fehler":
                url = fehler + "#" + urllib.parse.quote(json.dumps(k.get("fehler", {"domain": k.get("domain", "")}), ensure_ascii=False))
                shot(pc, url, out / f"{s}-alt-pc.png", 200)
                shot(ha, url, out / f"{s}-alt-handy.png", 200)
            else:
                url = vorher + "#" + urllib.parse.quote(json.dumps(k["suche"], ensure_ascii=False))
                shot(pc, url, out / f"{s}-alt-pc.png", 200)
                shot(ha, url, out / f"{s}-alt-handy.png", 200)
            print(f"✓ {k['name']}  ({n} Handy-Bildschirme)")
        b.close()
