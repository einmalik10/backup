---
description: Einrichtung ohne Scan (Python, Playwright, kurze Fragen)
---
Richte die Umgebung ein. **Starte keinen Scan.**

1. Prüfe Git und Python (`python --version`) und installiere bei Bedarf nach Rückfrage: `python -m pip install requests jinja2 playwright pillow`, dann `python -m playwright install chromium` im Hintergrund.
2. Frag in **einer** Nachricht: Name für Mappen (oder leer), Telefon für Mappen (optional, nur lokal), mit welchem Ort aus `gebiete.json` er anfangen will (Vorschlag: einer mit prio 1), Anrede gegenüber Läden (Vorschlag: Sie).
3. Speichere `notizen/mein-setup.md` (ohne Telefon) und `arbeit/absender.json` (lokal).
4. Erkläre in einem Satz das Gebiet: Großraum Tübingen laut `gebiete.json`, Sperrgebiete anderer Teams in `sperrgebiete.json`.
5. Zum Schluss in 4 Zeilen: was eingerichtet ist, und dass `/dashboard <Ort>` die Suche startet, wenn er bereit ist.
