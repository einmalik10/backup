# Webdesign Beginner · Großraum Tübingen

Einstieg: Websites für lokale Läden finden, zeigen und bauen, mit Claude Code.
**Modell:** einmal bauen, übergeben, kein Abo. Preisvorschlag in `docs/preise.md`.

## Start (10 Minuten)
1. Installieren: **Git** (git-scm.com) und **Claude Code** (claude.com/claude-code).
2. Den Text aus `STARTPROMPT.md` in eine neue Claude-Code-Sitzung kopieren.
3. Claude richtet alles ein und fragt dich kurz nach deinen Angaben. **Es sucht noch keine Läden.**
4. Wenn du bereit bist: `/dashboard Rottenburg am Neckar` (oder ein anderer Ort aus `gebiete.json`).

## Befehle
- `/einrichten`: Einrichtung ohne Suche
- `/dashboard <Ort>`: Läden finden, prüfen, Dashboard im Browser
- `/mappe <Laden>`: Demo und Mappe zum Zeigen
- `/website <Laden>`: nach einer Zusage die echte Website

## Zusätzliche Skills (in `.claude/skills/`)
Claude nutzt sie automatisch, wenn die Aufgabe passt.
- **Websites prüfen und verbessern** (aus [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), MIT): `frontend-ui-engineering`, `performance-optimization`, `browser-testing-with-devtools`, `security-and-hardening`, `shipping-and-launch`, `code-review-and-quality`. Checklisten in `agent-skills-references/`.
- **Videos aus HTML** (aus [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes), Apache-2.0): `hyperframes`, `hyperframes-cli`. Braucht Node.js 22+, FFmpeg (`winget install --id Gyan.FFmpeg -e`) und `npm install -g hyperframes@0.8.209`. Nutzungsdaten abschalten: Umgebungsvariable `HYPERFRAMES_NO_TELEMETRY=1`.

Herkunft, Stand und was weggelassen wurde: `QUELLE.md` in `agent-skills-references/` und `hyperframes/`.

## Dein Gebiet
**Großraum Tübingen**: Tübingen (Kernstadt und Teilorte), Reutlingen, Metzingen, Rottenburg, Mössingen, Herrenberg, Kirchentellinsfurt, Kusterdingen, Ammerbuch, Dußlingen, Gomaringen und weitere (`gebiete.json`).
Gebiete anderer Teams stehen in `sperrgebiete.json` (zurzeit Mannheim). Dort sucht Claude nicht.

## Regeln
- Keine Werbe-Mail oder Werbe-WhatsApp ohne vorheriges Ja (§ 7 UWG).
- Nur Kritik, die man am Screenshot sieht.
- Immer mit Rechnung, Gewerbe vorher anmelden.
- Kundendaten nie ins Repo (`arbeit/` bleibt lokal).
