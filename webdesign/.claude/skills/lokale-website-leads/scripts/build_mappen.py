"""Baut pro Kunde eine Pitch-Mappe als HTML und PDF (A4, 5 Seiten).

Aufruf:
    python build_mappen.py --kunden kunden.py --out mappen [--datum "Oktober 2026"] [slug ...]

Erwartet die Bilder aus shots.py in <out>/img/. Ergebnis: <out>/Mappe-<slug>.html und .pdf.
Danach mindestens Seite 1 und 2 einer Mappe rendern und ansehen (siehe SKILL.md, Prüfen).
"""
import argparse
import datetime
import importlib.util
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

HIER = Path(__file__).resolve().parent
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]


def lade_kunden(pfad):
    spec = importlib.util.spec_from_file_location("kunden", pfad)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.KUNDEN, getattr(m, "ABSENDER", {"name": "[Ihr Name]", "telefon": "[Telefon]", "zusatz": ""})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--kunden", required=True)
    ap.add_argument("--out", default="mappen")
    ap.add_argument("--vorlage", default=str(HIER.parent / "assets" / "mappe.html"))
    ap.add_argument("--datum")
    ap.add_argument("--vorschau", action="store_true", help="zusätzlich jede Seite als PNG (vorschau-<slug>-<n>.png) zum Prüfen")
    ap.add_argument("slugs", nargs="*")
    a = ap.parse_args()
    heute = datetime.date.today()
    datum = a.datum or f"{MONATE[heute.month - 1]} {heute.year}"
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    vorlage = Path(a.vorlage)
    tpl = Environment(loader=FileSystemLoader(vorlage.parent), autoescape=True).get_template(vorlage.name)
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 800, "height": 1131})
        kunden, absender = lade_kunden(a.kunden)
        for k in kunden:
            if a.slugs and k["slug"] not in a.slugs:
                continue
            teile = sorted((out / "img").glob(f"{k['slug']}-neu-handy-s*.png"), key=lambda q: int(q.stem.rsplit("s", 1)[1]))
            k["handy_teile"] = [f"img/{q.name}" for q in teile]
            html = out / f"Mappe-{k['slug']}.html"
            html.write_text(tpl.render(k=k, datum=datum, absender=absender), encoding="utf-8")
            page.goto(html.resolve().as_uri(), wait_until="networkidle")
            page.wait_for_timeout(800)
            page.pdf(path=str(out / f"Mappe-{k['slug']}.pdf"), format="A4", print_background=True, prefer_css_page_size=True)
            if a.vorschau:
                for i, el in enumerate(page.query_selector_all("section.page"), 1):
                    el.screenshot(path=str(out / f"vorschau-{k['slug']}-{i}.png"))
            print("✓", k["name"])
        b.close()
