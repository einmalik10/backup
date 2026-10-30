"""Baut eine fertige Demo-Website aus einer Kundendatei.

Aufruf:
    python build.py kunden/beispiel-beauty.json
    python build.py kunden/*.json          (alle auf einmal)

Ergebnis: out/<slug>/index.html, impressum.html, datenschutz.html, fonts/, Bilder.
Bilder legst du neben die JSON-Datei in kunden/<slug>/ und nennst sie in "bilder".
"""
import datetime
import glob
import os
import json
import re
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, ChainableUndefined

def lang(p):
    """Windows: Pfade über 260 Zeichen erlauben."""
    p = Path(p).resolve()
    return Path("\\\\?\\" + str(p)) if os.name == "nt" and not str(p).startswith("\\\\?\\") else p


ROOT = lang(Path(__file__).parent)
TAGE = ["mo", "di", "mi", "do", "fr", "sa", "so"]
TAG_NAMEN = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
TAG_KURZ = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

FONTS = {
    "beauty": [("Cormorant Garamond", 500), ("Cormorant Garamond", 600), ("Jost", 400), ("Jost", 500), ("Jost", 600)],
    "gastro": [("Young Serif", 400), ("Hanken Grotesk", 400), ("Hanken Grotesk", 600), ("Hanken Grotesk", 700)],
    "praxis": [("Atkinson Hyperlegible", 400), ("Atkinson Hyperlegible", 700)],
}
SCHEMA_TYP = {"beauty": "BeautySalon", "gastro": "Restaurant", "praxis": "MedicalClinic"}

_svg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
ICONS = {
    "phone": _svg.format('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>'),
    "route": _svg.format('<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>'),
    "calendar": _svg.format('<rect x="3" y="4.5" width="18" height="16.5" rx="2"/><path d="M16 2.5v4M8 2.5v4M3 10h18"/>'),
    "list": _svg.format('<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>'),
    "chat": _svg.format('<path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.5L3 21l2-5.4A8.4 8.4 0 1 1 21 11.5z"/>'),
}


def minuten(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def zeiten(oeffnung):
    """{"mo": ["09:00-18:00"], "di": [...], ...} -> Tabelle + JS-Daten. Fehlender Tag = geschlossen."""
    rows, js = [], []
    for i, tag in enumerate(TAGE):
        spannen = oeffnung.get(tag) or []
        js.append([[minuten(a), minuten(b)] for a, b in (s.split("-") for s in spannen)])
        text = " und ".join(s.replace("-", "–") for s in spannen) if spannen else "geschlossen"
        rows.append({"idx": i, "name": TAG_NAMEN[i], "text": text})
    return rows, js


def text_farbe(hex_farbe):
    """Weiß oder Fast-Schwarz, je nachdem was auf der Markenfarbe lesbarer ist."""
    h = hex_farbe.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    lum = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    return "#ffffff" if (1.05 / (lum + 0.05)) >= 4.5 else "#141414"


def cta(s):
    b = s["branche"]
    label, kurz = {"beauty": ("Termin buchen", "Buchen"), "gastro": ("Tisch reservieren", "Reservieren"), "praxis": ("Termin vereinbaren", "Termin")}[b]
    url = s.get("buchung_url") or s.get("reservierung_url") or s.get("termin_url")
    if url:
        return {"href": url, "ext": True, "label": label, "short": kurz, "icon": "calendar"}
    if s.get("whatsapp"):
        return {"href": "https://wa.me/" + re.sub(r"\D", "", s["whatsapp"]), "ext": True, "label": label + " per WhatsApp", "short": "WhatsApp", "icon": "chat"}
    return {"href": "tel:" + tel(s["telefon"]), "ext": False, "label": label + " per Telefon", "short": kurz, "icon": "phone"}


def tel(nummer):
    n = re.sub(r"[^\d+]", "", nummer)
    return "+49" + n[1:] if n.startswith("0") else n


def schema(s, js):
    oh = []
    for i, spannen in enumerate(js):
        for a, b in spannen:
            oh.append(f"{TAG_KURZ[i][:2]} {a // 60:02d}:{a % 60:02d}-{b // 60:02d}:{b % 60:02d}")
    d = {"@context": "https://schema.org", "@type": SCHEMA_TYP[s["branche"]], "name": s["name"], "telephone": s["telefon"],
         "address": {"@type": "PostalAddress", "streetAddress": s["adresse"]["strasse"], "postalCode": s["adresse"]["plz"], "addressLocality": s["adresse"]["ort"], "addressCountry": "DE"},
         "openingHours": oh}
    if s.get("domain"):
        d["url"] = "https://" + s["domain"]
    if s["branche"] == "gastro" and s.get("kueche"):
        d["servesCuisine"] = s["kueche"]
    return d


def build(pfad):
    pfad = lang(pfad)
    s = json.loads(pfad.read_text(encoding="utf-8"))
    for pflicht in ("branche", "slug", "name", "telefon", "adresse", "farbe", "oeffnungszeiten"):
        if pflicht not in s:
            sys.exit(f"{pfad.name}: Feld '{pflicht}' fehlt")
    b = s["branche"]
    if b not in FONTS:
        sys.exit(f"{pfad.name}: branche muss beauty, gastro oder praxis sein")
    s.setdefault("bilder", {})
    s.setdefault("impressum", {})
    s.setdefault("claim", {"beauty": "Friseur in ", "gastro": "Restaurant in ", "praxis": "Praxis in "}[b] + s["adresse"]["ort"])
    rows, js = zeiten(s["oeffnungszeiten"])
    s["schema"] = schema(s, js)
    m = re.match(r"^\s*([A-UX-Z])\s?(\d{1,2})\b", s["adresse"]["strasse"])
    fonts = FONTS[b]
    faces = [{"family": f, "weight": w, "file": f"{f.lower().replace(' ', '-')}-{w}.woff2"} for f, w in fonts]
    adresse = f'{s["adresse"]["strasse"]}, {s["adresse"]["plz"]} {s["adresse"]["ort"]}'
    ctx = dict(
        s=s, hours=rows, hours_json=json.dumps(js), day_names_json=json.dumps(TAG_NAMEN, ensure_ascii=False),
        quadrat=(m.group(1) + m.group(2)) if m else "", brand_ink=text_farbe(s["farbe"]),
        tel_link=tel(s["telefon"]), cta=cta(s), icons=ICONS, font_faces=faces, fonts=[faces[0]["file"]],
        maps_url=s.get("maps_url") or "https://www.google.com/maps/search/?api=1&query=" + (s["name"] + " " + adresse).replace(" ", "+"),
        zeiten_label="Sprechzeiten" if b == "praxis" else "Öffnungszeiten", jahr=datetime.date.today().year,
        branche_template=f"{b}.html", legal=None, home="",
        mitte={"beauty": {"href": "#preise", "label": "Preise"}, "gastro": {"href": "#karte", "label": "Karte"}, "praxis": {"href": "#leistungen", "label": "Leistungen"}}[b],
    )
    env = Environment(loader=FileSystemLoader(Path(__file__).resolve().parent / "templates"), autoescape=True, undefined=ChainableUndefined, trim_blocks=True, lstrip_blocks=True)
    out = ROOT / "out" / s["slug"]
    if out.exists():
        shutil.rmtree(out)
    (out / "fonts").mkdir(parents=True)
    (out / "index.html").write_text(env.get_template(f"{b}.html").render(**ctx), encoding="utf-8")
    for legal, titel in (("impressum", "Impressum"), ("datenschutz", "Datenschutz")):
        (out / f"{legal}.html").write_text(env.get_template("legal.html").render(**{**ctx, "legal": legal, "legal_title": titel, "home": "index.html"}), encoding="utf-8")
    for f in faces:
        shutil.copy(ROOT / "assets" / "fonts" / f["file"], out / "fonts" / f["file"])
    bild_ordner = pfad.parent / s["slug"]
    if bild_ordner.is_dir():
        shutil.copytree(bild_ordner, out, dirs_exist_ok=True)
    fehlt = [str(x) for x in [s["bilder"].get("hero")] + list(s["bilder"].get("galerie", [])) if x and not (out / x).exists()]
    print(f"✓ {s['name']:<28} → out/{s['slug']}/index.html" + (f"   (Bilder fehlen: {', '.join(fehlt)})" if fehlt else ""))


if __name__ == "__main__":
    dateien = [p for a in sys.argv[1:] for p in (glob.glob(a) or [a])]
    if not dateien:
        sys.exit(__doc__)
    for d in dateien:
        build(d)
