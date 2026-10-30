"""Screenshots der HEUTIGEN Websites von Kandidaten + ein Kontaktbogen zum schnellen Sichten.

Aufruf:
    python sichten.py --out img slug1=https://seite1.de slug2=http://seite2.de ...

Erzeugt img/<slug>-alt-pc.png (1440x900), img/<slug>-alt-handy.png (390x844, iPhone)
und kontaktbogen.png mit allen nebeneinander. Den Kontaktbogen mit dem Read-Tool ansehen,
danach die besten Kandidaten einzeln in voller Größe öffnen und Befunde prüfen.
"""
import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# Normale Chrome-Kennung: viele Hoster (z. B. IONOS) antworten "HeadlessChrome" mit 503/403, das wäre ein falscher Befund
DESKTOP = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="img")
    ap.add_argument("paare", nargs="+", help="slug=url")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    paare = [p.split("=", 1) for p in a.paare]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pc = b.new_context(viewport={"width": 1440, "height": 900}, locale="de-DE", user_agent=DESKTOP).new_page()
        ha = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
                           locale="de-DE", user_agent=IPHONE).new_page()
        for slug, url in paare:
            for page, n in ((pc, "pc"), (ha, "handy")):
                try:
                    page.goto(url, wait_until="load", timeout=30000)
                    page.wait_for_timeout(1800)
                    page.screenshot(path=str(out / f"{slug}-alt-{n}.png"))
                except Exception as e:
                    print(f"  {slug} {n}: {type(e).__name__} (Seite nicht erreichbar? Das ist selbst ein Befund)")
            print("ok", slug)
        h = '<html><body style="margin:0;background:#333;font:14px sans-serif;color:#fff;display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:6px">'
        for slug, _ in paare:
            h += (f'<div><div>{slug}</div><div style="display:flex;gap:4px"><img src="{out.name}/{slug}-alt-pc.png" style="width:280px">'
                  f'<img src="{out.name}/{slug}-alt-handy.png" style="width:90px;height:175px;object-fit:cover;object-position:top"></div></div>')
        bogen = out.parent / "kontaktbogen.html"
        bogen.write_text(h + "</body></html>", encoding="utf-8")
        pg = b.new_page(viewport={"width": 1520, "height": 420})
        pg.goto(bogen.resolve().as_uri()); pg.wait_for_timeout(500)
        pg.screenshot(path=str(out.parent / "kontaktbogen.png"), full_page=True)
        b.close()
    print("→ kontaktbogen.png")
