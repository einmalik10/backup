"""Vorher/Nachher-Screenshots einer Website: alte und neue Version nebeneinander, am PC und am Handy.

Ablauf:
    1. Vor der Änderung den gebauten Ordner sichern:
           python vergleich.py --sichern <kunde>/dist
       → kopiert nach <kunde>/sicherung/vergleich-<datum-uhrzeit>/dist und zeigt den Pfad.
    2. Ändern und neu bauen.
    3. Vergleichen:
           python vergleich.py <alt-ordner> <neu-ordner> [--seiten index,sortiment] [--abschnitt index:#besuch ...] [--out <ordner>]

Ergebnis im Ausgabeordner (Standard: <neu-ordner>/../vergleich/<datum-uhrzeit>/):
    <seite>-pc-start.png      erster Bildschirm (1440 × 900)
    <seite>-handy-start.png   erster Bildschirm (390 × 844)
    <seite>-pc-ganz.png       ganze Seite, beide im selben Maßstab (Länge vergleichbar)
    <seite>-handy-ganz.png
    <seite>-<geraet>-<abschnitt>.png   bei --abschnitt: Ausschnitt ab diesem Element
Dazu eine Tabelle mit Seitenlängen und eine Prüfung auf waagrechtes Scrollen (neue Version).

Beide Ordner werden für die Dauer des Laufs über einen lokalen Server ausgeliefert. Nichts verlässt den Rechner.
Braucht playwright und pillow.
"""
import argparse
import functools
import http.server
import shutil
import sys
import threading
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

GERAETE = {"pc": {"width": 1440, "height": 900}, "handy": {"width": 390, "height": 844}}
MAX_HOEHE = 6000   # ganze Seiten werden höchstens so hoch ausgegeben (beide im selben Maßstab)


def schrift(groesse):
    for name in ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, groesse)
        except OSError:
            continue
    return ImageFont.load_default()


class StillerHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class StillerServer(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        pass   # abgebrochene Verbindungen beim Schließen des Browsers sind normal


def server(ordner):
    handler = functools.partial(StillerHandler, directory=str(ordner))
    srv = StillerServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def laden(pg, url):
    pg.goto(url)
    pg.wait_for_timeout(500)
    h = pg.evaluate("document.documentElement.scrollHeight")
    for y in range(0, h, 600):   # Lazy-Bilder laden
        pg.evaluate(f"scrollTo(0,{y})")
        pg.wait_for_timeout(50)
    pg.evaluate("scrollTo(0,0)")
    pg.wait_for_timeout(400)


def feste_ausblenden(pg):
    """Feste Leisten (z. B. Anrufleiste) stören ganzseitige Screenshots, weil sie mitten im Bild landen."""
    pg.evaluate("""() => document.querySelectorAll('body *').forEach(e => {
        if (getComputedStyle(e).position === 'fixed') e.style.visibility = 'hidden'; })""")


def paar(alt, neu, ziel, titel="", massstab=1.0):
    a, b = Image.open(alt), Image.open(neu)
    if massstab != 1.0:
        a = a.resize((int(a.width * massstab), int(a.height * massstab)))
        b = b.resize((int(b.width * massstab), int(b.height * massstab)))
    rand, kopf = 24, 76
    bild = Image.new("RGB", (a.width + b.width + 3 * rand, max(a.height, b.height) + kopf + rand), "#e9e6e0")
    d = ImageDraw.Draw(bild)
    f, fk = schrift(30), schrift(18)
    d.text((rand, 16), "VORHER", font=f, fill="#a3162a")
    d.text((2 * rand + a.width, 16), "NACHHER", font=f, fill="#128747")
    if titel:
        d.text((rand, 52), titel, font=fk, fill="#56605a")
    bild.paste(a, (rand, kopf))
    bild.paste(b, (2 * rand + a.width, kopf))
    bild.save(ziel)


def sichern(dist):
    dist = Path(dist).resolve()
    if not dist.is_dir():
        sys.exit(f"Ordner nicht gefunden: {dist}")
    ziel = dist.parent / "sicherung" / f"vergleich-{datetime.now():%Y-%m-%d-%H%M}" / dist.name
    shutil.copytree(dist, ziel)
    print(f"gesichert: {ziel}\nNach der Änderung: python vergleich.py \"{ziel}\" \"{dist}\"")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("alt", nargs="?")
    ap.add_argument("neu", nargs="?")
    ap.add_argument("--sichern", metavar="DIST", help="gebauten Ordner vor der Änderung sichern")
    ap.add_argument("--seiten", help="Komma-Liste ohne .html (Standard: alle Seiten außer 404, impressum, datenschutz, danke, fehler)")
    ap.add_argument("--abschnitt", action="append", default=[], metavar="SEITE:SELEKTOR",
                    help="zusätzlich einen Ausschnitt ab diesem Element, z. B. index:#besuch (mehrfach möglich)")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.sichern:
        return sichern(a.sichern)
    if not (a.alt and a.neu):
        ap.error("alt- und neu-Ordner angeben (oder --sichern)")
    alt, neu = Path(a.alt).resolve(), Path(a.neu).resolve()
    out = Path(a.out) if a.out else neu.parent / "vergleich" / f"{datetime.now():%Y-%m-%d-%H%M}"
    roh = out / "roh"
    roh.mkdir(parents=True, exist_ok=True)

    weg = {"404", "impressum", "datenschutz", "danke", "fehler"}
    seiten = a.seiten.split(",") if a.seiten else sorted(p.stem for p in neu.glob("*.html") if p.stem not in weg)
    abschnitte = [x.split(":", 1) for x in a.abschnitt]

    srv_alt, url_alt = server(alt)
    srv_neu, url_neu = server(neu)
    zeilen, ueberlauf = [], []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for geraet, vp in GERAETE.items():
            mobil = geraet == "handy"
            # Service-Worker blockieren: sonst zeigt eine App-Seite evtl. zwischengespeicherte alte Dateien
            ctx = b.new_context(viewport=vp, is_mobile=mobil, has_touch=mobil, reduced_motion="reduce", service_workers="block")
            pg = ctx.new_page()
            for seite in seiten:
                hoehen = {}
                for tag, basis, ordner in (("alt", url_alt, alt), ("neu", url_neu, neu)):
                    if not (ordner / f"{seite}.html").exists():
                        hoehen[tag] = None
                        continue
                    laden(pg, f"{basis}/{seite}.html")
                    pg.screenshot(path=roh / f"{tag}-{seite}-{geraet}-start.png")
                    if tag == "neu" and pg.evaluate("document.documentElement.scrollWidth > innerWidth"):
                        ueberlauf.append(f"{seite} ({geraet})")
                    for sel_seite, sel in abschnitte:
                        if sel_seite != seite:
                            continue
                        y = pg.evaluate(f"(() => {{ const e = document.querySelector({sel!r}); return e ? e.getBoundingClientRect().top + scrollY : null; }})()")
                        if y is not None:
                            feste_ausblenden(pg)
                            pg.screenshot(path=roh / f"{tag}-{seite}-{geraet}-{sel.strip('#.')}.png", full_page=True,
                                          clip={"x": 0, "y": y, "width": vp["width"], "height": min(1600, pg.evaluate("document.documentElement.scrollHeight") - y)})
                            laden(pg, f"{basis}/{seite}.html")
                    feste_ausblenden(pg)
                    hoehen[tag] = pg.evaluate("document.documentElement.scrollHeight")
                    pg.screenshot(path=roh / f"{tag}-{seite}-{geraet}-ganz.png", full_page=True)
                if None in hoehen.values():
                    print(f"  ! {seite}.html fehlt in {'alt' if hoehen.get('alt') is None else 'neu'}, übersprungen")
                    continue
                zeilen.append((seite, geraet, hoehen["alt"], hoehen["neu"]))
                pc_scale = 0.62 if geraet == "pc" else 1.0
                paar(roh / f"alt-{seite}-{geraet}-start.png", roh / f"neu-{seite}-{geraet}-start.png",
                     out / f"{seite}-{geraet}-start.png", f"{seite}.html · erster Bildschirm", pc_scale)
                ganz = min(pc_scale, MAX_HOEHE / max(hoehen.values()))
                paar(roh / f"alt-{seite}-{geraet}-ganz.png", roh / f"neu-{seite}-{geraet}-ganz.png",
                     out / f"{seite}-{geraet}-ganz.png", f"{seite}.html · ganze Seite: {hoehen['alt']} → {hoehen['neu']} px", ganz)
                for sel_seite, sel in abschnitte:
                    name = f"{seite}-{geraet}-{sel.strip('#.')}.png"
                    if sel_seite == seite and (roh / f"alt-{name}").exists() and (roh / f"neu-{name}").exists():
                        paar(roh / f"alt-{name}", roh / f"neu-{name}", out / name, f"{seite}.html · {sel}", pc_scale)
            ctx.close()
        b.close()
    srv_alt.shutdown()
    srv_neu.shutdown()
    shutil.rmtree(roh)

    print(f"{'Seite':<14}{'Gerät':<8}{'vorher':>9}{'nachher':>9}{'Änderung':>10}")
    for seite, geraet, h_alt, h_neu in zeilen:
        print(f"{seite:<14}{geraet:<8}{h_alt:>7} px{h_neu:>7} px{(h_neu - h_alt) / h_alt:>+10.0%}")
    print("✗ Waagrechtes Scrollen (neu): " + ", ".join(ueberlauf) if ueberlauf else "✓ Kein waagrechtes Scrollen (neu)")
    print(f"Bilder: {out}")


if __name__ == "__main__":
    main()
