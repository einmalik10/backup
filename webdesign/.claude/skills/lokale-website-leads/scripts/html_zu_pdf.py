"""Wandelt eine HTML-Datei in ein A4-PDF um (z. B. Preisliste).

Aufruf:
    python html_zu_pdf.py eingabe.html ausgabe.pdf

Braucht playwright (siehe docs/tools.md). Hintergrundfarben und Schriften werden mit gedruckt.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

if len(sys.argv) != 3:
    sys.exit(__doc__)
quelle, ziel = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(quelle.as_uri())
    pg.wait_for_timeout(500)
    pg.pdf(path=str(ziel), format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
print("geschrieben:", ziel)
