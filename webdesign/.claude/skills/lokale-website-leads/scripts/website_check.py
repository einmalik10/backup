"""Prüft eine fertige Website (Ordner mit HTML-Dateien) gegen den Website-Standard (references/website-standard.md).

Aufruf:
    python website_check.py <ordner> [--live]      # --live: noindex und [FEHLT]/[PRÜFEN] sind Fehler statt Warnung

Ausgabe: ✗ = Fehler (vor dem Livegang beheben), ! = Warnung (bewusst entscheiden), ✓ = ok.
Exit-Code 1, wenn es Fehler gibt.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

IGNORIEREN = {"danke.html", "fehler.html"}


class Seite(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self._in_title = False
        self.meta = {}; self.links = []; self.h1 = 0; self.imgs = []; self.ids = []
        self.scripts = []; self._in_ld = False; self.ld = []; self.lang = None
        self.inputs = []; self.labels_for = set(); self.ext = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k.lower()] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
            if a.get("rel") == "stylesheet" and re.match(r"https?://", a.get("href", "")):
                self.ext.append(a["href"])
        elif tag == "h1":
            self.h1 += 1
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "script":
            if a.get("type") == "application/ld+json":
                self._in_ld = True; self.ld.append("")
            elif re.match(r"https?://", a.get("src", "")):
                self.ext.append(a["src"])
        elif tag in ("input", "select", "textarea") and a.get("type") not in ("hidden", "submit", "radio", "checkbox"):
            if "website" not in (a.get("name") or ""):
                self.inputs.append(a.get("id"))
        elif tag == "label" and a.get("for"):
            self.labels_for.add(a["for"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script":
            self._in_ld = False

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        if self._in_ld:
            self.ld[-1] += d


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # Windows-Konsole kann sonst ✓/✗ nicht ausgeben
    ap = argparse.ArgumentParser()
    ap.add_argument("ordner")
    ap.add_argument("--live", action="store_true")
    a = ap.parse_args()
    root = Path(a.ordner)
    seiten = sorted(p for p in root.rglob("*.html") if "node_modules" not in p.parts)
    if not seiten:
        sys.exit("Keine HTML-Dateien gefunden.")
    fehler = warn = 0

    def f(msg):
        nonlocal fehler; fehler += 1; print("  ✗", msg)

    def w(msg):
        nonlocal warn; warn += 1; print("  !", msg)

    titel_alle = {}
    for p in seiten:
        rel = p.relative_to(root).as_posix()
        html = p.read_text(encoding="utf-8", errors="replace")
        s = Seite(); s.feed(html)
        print(rel)
        oeffentlich = p.name not in IGNORIEREN
        t = s.title.strip()
        if not t:
            f("kein <title>")
        else:
            titel_alle.setdefault(t, []).append(rel)
            if oeffentlich and not (25 <= len(t) <= 65):
                w(f"Titel {len(t)} Zeichen (ideal 50–60): {t}")
        d = s.meta.get("description", "")
        if oeffentlich:
            if not d:
                f("keine meta description")
            elif not (70 <= len(d) <= 170):
                w(f"Description {len(d)} Zeichen (ideal 120–160)")
        if s.h1 != 1 and oeffentlich:
            f(f"{s.h1} × <h1> (genau 1)")
        if not s.lang:
            f('<html lang="…"> fehlt')
        if oeffentlich and not any(l.get("rel") == "canonical" for l in s.links):
            w("kein canonical-Link")
        if "viewport" not in s.meta:
            f("kein viewport-Meta (Handy)")
        if p.name == "index.html":
            if not s.ld:
                f("kein JSON-LD (LocalBusiness/Restaurant …) auf der Startseite")
            for blob in s.ld:
                try:
                    j = json.loads(blob)
                    for feld in ("name", "address", "telephone"):
                        if feld not in j:
                            f(f"JSON-LD: Feld '{feld}' fehlt")
                    if "openingHoursSpecification" not in j and "openingHours" not in j:
                        w("JSON-LD: Öffnungszeiten fehlen")
                except Exception as e:
                    f(f"JSON-LD ungültig: {e}")
            if "og:image" not in s.meta:
                w("kein og:image (Vorschau in WhatsApp)")
        for img in s.imgs:
            src = img.get("src", "?")
            if "alt" not in img:
                f(f"Bild ohne alt: {src}")
            if not (img.get("width") and img.get("height")):
                w(f"Bild ohne width/height: {src}")
            q = (p.parent / src)
            if q.exists() and q.stat().st_size > 300_000:
                w(f"Bild > 300 KB: {src} ({q.stat().st_size // 1024} KB)")
        for i in s.inputs:
            if i and i not in s.labels_for:
                w(f"Formularfeld ohne <label for>: #{i}")
            if not i:
                w("Formularfeld ohne id/label")
        doppelt = {i for i in s.ids if s.ids.count(i) > 1}
        if doppelt:
            f("doppelte ids: " + ", ".join(sorted(doppelt)))
        for e in s.ext:
            if "fonts.googleapis" in e or "fonts.gstatic" in e:
                f(f"Google Fonts extern geladen (DSGVO): {e[:60]}")
            else:
                w(f"externe Ressource: {e[:70]}")
        if re.search(r'name=["\']robots["\'][^>]*noindex', html):
            (f if a.live else w)("noindex gesetzt (vor Livegang entfernen)")
        offen = len(re.findall(r"\[(FEHLT|PRÜFEN|PRUEFEN)", html))
        if offen:
            (f if a.live else w)(f"{offen} offene [FEHLT]/[PRÜFEN]-Markierungen")
        if re.search(r"!important", html):
            w("!important im Inline-CSS")

    print("Gesamt")
    for t, wo in titel_alle.items():
        if len(wo) > 1:
            f(f"gleicher Titel auf {', '.join(wo)}")
    for datei in ("robots.txt", "sitemap.xml"):
        if not (root / datei).exists():
            f(f"{datei} fehlt")
    if not (root / "404.html").exists():
        w("404.html fehlt")
    if not any((root / n).exists() for n in ("impressum.html", "impressum/index.html")):
        f("impressum.html fehlt")
    if not any((root / n).exists() for n in ("datenschutz.html", "datenschutz/index.html")):
        f("datenschutz.html fehlt")
    for css in root.rglob("*.css"):
        c = css.read_text(encoding="utf-8", errors="replace")
        if ":root" not in c:
            w(f"{css.name}: keine Design-Tokens in :root")
        if "!important" in c:
            w(f"{css.name}: !important verwendet")
        if "fonts.googleapis" in c:
            f(f"{css.name}: Google Fonts extern (DSGVO)")
    if not (root / "README.md").exists() and not (root.parent / "README.md").exists():
        w("README.md für Kunde/Nachfolger fehlt")
    print(f"\n{'✓ Keine Fehler' if not fehler else f'✗ {fehler} Fehler'} · {warn} Warnungen")
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
