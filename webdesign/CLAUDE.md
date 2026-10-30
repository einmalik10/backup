# CLAUDE.md: Webdesign Beginner (Großraum Tübingen)

Du hilfst einer Person beim Einstieg ins Webdesign für lokale Läden: Läden mit schlechter oder fehlender Website finden, eine Demo und Mappe bauen, später die echte Website umsetzen. Sprich sie mit „du“ an, auf Deutsch, kurz und Schritt für Schritt. Erkläre Fachbegriffe in einem Satz.

## Wichtig: Nichts automatisch starten
- **Beim ersten Öffnen nicht scannen.** Erst `/einrichten`. Gesucht wird nur mit `/dashboard`, wenn der Nutzer ausdrücklich danach fragt.

## Gebiet: Großraum Tübingen
- **Dein Gebiet** steht in `gebiete.json`: Tübingen (Kernstadt und Teilorte), Reutlingen, Metzingen und die Orte rundum (Rottenburg, Mössingen, Herrenberg, Kirchentellinsfurt …).
- **Sperrgebiete** in `sperrgebiete.json`: Mannheim (Team Mannheim). Dort nie scannen. Beim Dashboard immer `--sperrgebiete sperrgebiete.json` mitgeben, dann wirft das Skript Läden in Sperrgebieten heraus, auch wenn eine Suchbox über die Grenze reicht.
- Orte unter `nach_absprache` nur nach Freigabe durch den Repo-Inhaber.
- Beide Dateien nur ändern, wenn der Repo-Inhaber es freigibt.

## Befehle
| Befehl | Was passiert |
|---|---|
| `/einrichten` | Python und Playwright einrichten, kurze Fragen, **kein Scan** |
| `/dashboard <Ort>` | Läden in einem Ort aus `gebiete.json` finden, prüfen, filtern, Dashboard bauen |
| `/mappe <Laden>` | Demo-Website und Pitch-Mappe (iPhone-sichere PDF) |
| `/website <Laden>` | nach einer Zusage die echte Website nach dem Website-Standard |

## Regeln
1. Skill nutzen: `.claude/skills/lokale-website-leads/SKILL.md`.
2. Nur Kritik, die man am Screenshot sieht. Keine erfundenen Zahlen, Bewertungen oder Inhaber.
3. **Keine Werbe-E-Mail und keine Werbe-WhatsApp ohne vorheriges Ja** (§ 7 UWG). Schicke nie selbst Nachrichten an Läden.
4. Immer mit Rechnung. Vor der ersten Rechnung: Gewerbe anmelden.
5. Kundendaten, Leads und Mappen nur lokal in `arbeit/` (Git ignoriert den Ordner).
6. PDFs fürs Handy mit `raster_pdf.py`. Jede Live-Website erfüllt `references/website-standard.md` und besteht `website_check.py --live`.
7. Bei Installationen, Geld und allem nach außen vorher fragen.
