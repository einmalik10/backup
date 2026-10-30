"""Baut aus einer Mappen-HTML eine "gerasterte" PDF: jede Seite als scharfes Bild.

Warum: Browser-PDFs (page.pdf) sehen am PC gut aus, aber die iPhone-Vorschau
(Dateien, WhatsApp, Mail) stellt Webfonts, Verläufe, Überlagerungen und
object-fit oft falsch dar. Eine Bild-PDF sieht auf jedem Gerät identisch aus.
Text ist darin nicht markierbar, für eine Pitch-Mappe egal.

Aufruf:
    python raster_pdf.py Mappe-x.html [Mappe-y.html ...] [--scale 2] [--selector ".page, section.p"]

Erzeugt neben jeder HTML: <name>.pdf (überschreibt) und <name>-seiten/seite-N.jpg.
Ist die PDF gesperrt (geöffnet), wird <name>-neu.pdf geschrieben.
"""
import argparse
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("html", nargs="+")
ap.add_argument("--scale", type=float, default=2.0)
ap.add_argument("--selector", default=".page, section.p")
ap.add_argument("--quality", type=int, default=88)
a = ap.parse_args()

with sync_playwright() as p:
    b = p.chromium.launch()
    for h in a.html:
        h = Path(h).resolve()
        ctx = b.new_context(viewport={"width": 1000, "height": 1400}, device_scale_factor=a.scale)
        pg = ctx.new_page()
        pg.goto(h.as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(800)
        seiten = pg.query_selector_all(a.selector)
        if not seiten:
            print("✗ keine Seiten gefunden:", h.name); continue
        ordner = h.with_name(h.stem + "-seiten"); ordner.mkdir(exist_ok=True)
        bilder = []
        for i, s in enumerate(seiten, 1):
            f = ordner / f"seite-{i}.png"
            s.screenshot(path=str(f))
            im = Image.open(f).convert("RGB")
            im.save(f.with_suffix(".jpg"), "JPEG", quality=a.quality, optimize=True)
            f.unlink()
            bilder.append(im)
        dpi = 96 * a.scale  # 1 CSS-Pixel = 1/96 Zoll -> Seitengröße bleibt wie im Layout (z. B. A4)
        ziel = h.with_suffix(".pdf")
        try:
            bilder[0].save(ziel, "PDF", save_all=True, append_images=bilder[1:], resolution=dpi, quality=a.quality)
        except PermissionError:
            ziel = h.with_name(h.stem + "-neu.pdf")
            bilder[0].save(ziel, "PDF", save_all=True, append_images=bilder[1:], resolution=dpi, quality=a.quality)
        print(f"✓ {ziel.name}: {len(bilder)} Seiten, {ziel.stat().st_size // 1024} KB")
        ctx.close()
    b.close()
