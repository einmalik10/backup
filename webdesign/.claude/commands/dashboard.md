---
description: Läden in einem Ort der Tübinger Umgebung finden, filtern und Dashboard bauen (nur auf Wunsch)
---
Baue ein Lead-Dashboard für „$ARGUMENTS“. Fehlt der Ort, zeig die Orte aus `gebiete.json` (prio 1 zuerst) und frag.

1. **Gebiet prüfen:** Der Ort muss in `gebiete.json` stehen. Liegt er in `sperrgebiete.json` (z. B. Mannheim) oder unter `nach_absprache`: **abbrechen**, freundlich erklären, andere Orte vorschlagen.
**Ganzes Gebiet** (`/dashboard alle` oder „Großraum“): im Ordner `arbeit/grossraum/` mit
`python ../../.claude/skills/lokale-website-leads/scripts/fetch_gebiete.py --gebiete ../../gebiete.json --sperrgebiete ../../sperrgebiete.json --out osm.json`
(alle Orte aus `gebiete.json` per Gemeindegrenze, Teilorte per Box, Sperrgebiete und `nach_absprache` bleiben draußen). Danach weiter mit `audit.py --threads 4` und Schritt 3. Jeder Laden trägt sein Feld `ort`, das Board bekommt dann einen Ort-Filter.

2. Im Ordner `arbeit/<ort>/`:
   - `python ../../.claude/skills/lokale-website-leads/scripts/fetch_osm.py --area-name "<Ort>" --out osm.json`. Wenn Overpass ausfällt: Bbox um den Ortskern (ca. ±0,006° Breite, ±0,009° Länge).
   - `python ../../.claude/skills/lokale-website-leads/scripts/audit.py osm.json --out audit`
3. Vorauswahl nach den **Top-Lead-Kriterien** im Skill (Abschnitt 2): keine oder schlechte Website, inhabergeführt, keine Kette, aktiv, keine Arztpraxen oder Behörden. In kleinen Orten sind das oft nur 5–15 Läden, das ist okay. Lieber wenige gute als viele schlechte.
4. Prüfen: `sichten.py` für Screenshots, `inhaber.py` für Inhaber aus dem Impressum. Nur Belegtes in `pruefung.json`. Bei mehr als 25 Läden: günstige Haiku-Agenten (je 25), dann `merge_pruefung.py`.
5. Dashboard, **ein Board für alle seine Orte**: neue Orte in dieselbe `pruefung.json` und `audit.json` übernehmen (zusammenführen), dann:
   `python ../../.claude/skills/lokale-website-leads/scripts/build_leadboard.py --audit audit.json --pruefung pruefung.json --nur-geprueft --sperrgebiete ../../sperrgebiete.json --stadt "Tübingen-Umgebung" --untertitel "<Orte>" --out leadboard.html`
   Server mit `python -m http.server 8770` im Hintergrund starten und die Adresse nennen: `http://localhost:8770/leadboard.html`.
6. Abschluss: Top-Leads als Tabelle (Laden, Ort, Inhaber, Problem, Aufhänger) und der Tipp, mit `/mappe <Laden>` weiterzumachen.
