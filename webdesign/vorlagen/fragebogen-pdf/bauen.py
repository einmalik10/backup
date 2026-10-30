"""Baut den ausfüllbaren MI-Visuals-Projekt-Fragebogen als PDF.

Aufruf:
    python vorlagen/fragebogen-pdf/bauen.py [ausgabe.pdf]

1. Playwright druckt fragebogen.html als A4-PDF (Design).
2. PyMuPDF setzt auf jedes Element mit data-feld ein echtes Formularfeld:
   .f = Textfeld (.gross/.mittel mehrzeilig), .cb = Kästchen.
Ausfüllbar in Acrobat Reader, Vorschau (Mac), iPhone-Dateien-App und Chrome.
"""
import sys
from pathlib import Path

import pymupdf
from playwright.sync_api import sync_playwright

HIER = Path(__file__).resolve().parent
QUELLE = HIER / "fragebogen.html"
ZIEL = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HIER / "MI-Visuals-Projekt-Fragebogen.pdf"
PX_PRO_SEITE = 1123  # .page ist 794 × 1123 px = A4 bei 96 dpi
PT = 72 / 96          # px → PDF-Punkte

MESSEN = """() => {
  const seiten = [...document.querySelectorAll('.page')];
  const fehler = seiten.map((s, i) => s.scrollHeight > s.clientHeight + 1 ? i + 1 : 0).filter(Boolean);
  const felder = [...document.querySelectorAll('[data-feld]')].map(el => {
    const r = el.getBoundingClientRect(), s = el.closest('.page').getBoundingClientRect();
    return {name: el.dataset.feld, seite: seiten.indexOf(el.closest('.page')),
            x: r.left - s.left, y: r.top - s.top, w: r.width, h: r.height,
            art: el.classList.contains('cb') ? 'cb' : (el.offsetHeight > 50 ? 'multi' : 'text'),
            label: (el.closest('.frage, .k, .u, .skala')?.querySelector('.l')?.textContent
                    || el.closest('label, .skala')?.textContent || '').replace(/\\s+/g, ' ').trim()};
  });
  return {fehler, felder};
}"""


def main():
    tmp = ZIEL.with_suffix(".roh.pdf")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 794, "height": PX_PRO_SEITE})
        pg.goto(QUELLE.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(400)
        m = pg.evaluate(MESSEN)
        pg.pdf(path=str(tmp), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    if m["fehler"]:
        sys.exit(f"Inhalt läuft über auf Seite {m['fehler']} – Felder kleiner machen.")
    namen = [f["name"] for f in m["felder"]]
    doppelt = {n for n in namen if namen.count(n) > 1}
    if doppelt:
        sys.exit(f"Doppelte Feldnamen: {sorted(doppelt)}")

    doc = pymupdf.open(tmp)
    for f in m["felder"]:
        seite = doc[f["seite"]]
        r = pymupdf.Rect(f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]) * PT
        w = pymupdf.Widget()
        w.field_name = f["name"]
        w.field_label = f["label"][:120]
        w.border_width = 0
        w.fill_color = None
        if f["art"] == "cb":
            w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
            w.rect = r + (1.2, 1.2, -1.2, -1.2)
            w.text_color = (0.04, 0.04, 0.05)
            w.field_value = False
        else:
            w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
            w.rect = r + (6, 3, -6, -3)
            w.text_font = "Helv"
            w.text_color = (0.04, 0.04, 0.05)
            if f["art"] == "multi":
                w.field_flags |= pymupdf.PDF_TX_FIELD_IS_MULTILINE
                w.text_fontsize = 10
            else:
                w.text_fontsize = 10.5
        seite.add_widget(w)
    doc.set_metadata({"title": "MI Visuals · Projekt-Fragebogen", "author": "MI Visuals", "subject": "Fragebogen für deine neue Website"})
    doc.save(ZIEL, garbage=3, deflate=True)
    doc.close()
    tmp.unlink()
    print(f"geschrieben: {ZIEL} ({ZIEL.stat().st_size // 1024} KB, {len(m['felder'])} Felder)")


if __name__ == "__main__":
    main()
