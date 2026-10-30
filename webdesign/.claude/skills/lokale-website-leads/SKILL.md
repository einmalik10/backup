---
name: lokale-website-leads
description: >
  Findet lokale Läden mit schlechter oder fehlender Website (Restaurants, Cafés, Friseure, Praxen,
  Einzelhandel) in einer Stadt oder einem Viertel, prüft sie am echten Screenshot und baut pro Laden eine
  überzeugende Demo-Website und eine 5-seitige Pitch-Mappe (PDF): Website-Check mit roten Kritikpunkten,
  Entwurf auf PC und Handy, Design-Begründung und Angebot. Dazu Inhaber-Kontakte, Laufzettel für den
  Besuchstag, ein lokales Lead-Board (Dashboard) und rechtssichere Ansprache-Texte. Nutze diesen Skill immer, wenn jemand Webdesign-Kunden
  vor Ort gewinnen will, z. B. „welche Läden in X haben eine schlechte Website“, „Leads für Webdesign“,
  „Google Maps nach Läden scrapen“, „Demo-Seite für Laden Y“, „Pitch-Mappe / Vorher-Nachher“,
  „ich gehe heute nach Z“, „Kaltakquise Website verkaufen“, auch wenn das Wort „Lead“ nicht fällt.
---

# Lokale Website-Leads: finden, prüfen, Demo bauen, pitchen

Ziel: Der Inhaber eines Ladens soll beim ersten Blick auf die Mappe denken: „Stimmt, meine Seite ist
peinlich“ und beim Umblättern: „Wow, das bin ja ich.“ Dafür braucht es zwei Dinge:

1. **Wahrheit.** Jeder Kritikpunkt muss am echten Screenshot belegbar sein. Ein einziger falscher Punkt
   („Ihre Umlaute sind kaputt“, obwohl sie es nicht sind) beendet das Gespräch und kostet Glaubwürdigkeit.
2. **Eigenständigkeit.** Jede Demo hat ein eigenes Konzept aus Name, Schild, Geschichte oder dem stärksten
   Argument des Ladens. Keine Branchen-Vorlage mit ausgetauschtem Namen.

Kommuniziere mit dem Nutzer auf Deutsch, knapp, mit kurzen Zwischenständen bei langen Schritten.
Kundentexte immer in der Sie-Form, außer der Laden duzt selbst (z. B. „Dein Haarschnitt“).

## Werkzeuge und Einrichtung

- Python mit `requests`, `jinja2`, `playwright` (`python -m pip install requests jinja2 playwright`,
  dann `python -m playwright install chromium`, der Download dauert einige Minuten, also im Hintergrund starten).
- **Windows: Arbeitsordner mit kurzem Pfad**, z. B. `%TEMP%\leads\<stadt>`. Lange Pfade (Scratch-Ordner,
  AppData\Packages) überschreiten 260 Zeichen, dann scheitern Python, Bash-`cp` und die Artifact-Veröffentlichung.
  Fertige Ergebnisse am Schluss in den Projekt- oder Sitzungsordner kopieren.
- Lokaler Server für Demos: `python -m http.server 8765` im Demo-Elternordner, **im Hintergrund**
  (der Vorschau-Server der App kann ausfallen).
- Skripte in `scripts/` (`<skill>` = Ordner dieses Skills):
  - `fetch_osm.py`: Läden aus OpenStreetMap (bbox oder Gebietsname, mit Ausweichlösung bei überlastetem Overpass)
  - `audit.py`: automatischer Website-Check → `audit.json/.csv` (nur Vorfilter!)
  - `sichten.py`: Screenshots der heutigen Seiten + Kontaktbogen zum Sichten
  - `peek.py`: Text, Impressum, Inhaber, Preise einer Seite
  - `shots.py`: alle Mappen-Bilder (heute/neu, PC/Handy, komplette Handy-Seite)
  - `build_mappen.py`: Mappen als HTML + PDF (`--vorschau` für PNG-Kontrolle)
  - `build_leadboard.py`: Dashboard (Lead-Board) aus `audit.json` und `pruefung.json`
  - `html_zu_pdf.py`: beliebige HTML-Datei als A4-PDF (z. B. Preisliste)
  - `raster_pdf.py`: **iPhone-sichere PDF** aus Bildern der Seiten. Alles, was am Handy gezeigt oder per WhatsApp geschickt wird, so bauen.
  - `website_check.py`: prüft eine fertige Website gegen den Website-Standard (SEO, Architektur, DSGVO).
  - `vergleich.py`: Vorher/Nachher-Screenshots (PC und Handy, erster Bildschirm, ganze Seite, Ausschnitte) mit Seitenlängen und Überlauf-Prüfung. `--sichern dist` vor der Änderung.
  - `inhaber.py`: liest Inhaber/Geschäftsführer aus vielen Impressen parallel (ohne Tokens), `--einfuegen` schreibt in pruefung.json.
  - `merge_pruefung.py`: führt Ergebnisse der Haiku-Agenten (`res*.json`) in pruefung.json zusammen.
  - `raster_pdf.py`: **iPhone-sichere PDF** aus Bildern der Seiten (`python raster_pdf.py Mappe-x.html --selector ".page, section.p"`).
    Vektor-PDFs aus Chromium zeigen auf dem iPhone oft verschobene Schriften und Layouts. Mappen, die am Handy gezeigt werden, immer so bauen.
- Vorlagen in `assets/`: `mappe.html` (Pitch-Mappe), `vorher.html` (nachgestellte Suchansicht),
  `kunden_beispiel.py` (**Schema der Kundendatei, vor dem Schreiben lesen**), `baukasten/` (Vorlagen für echte Live-Seiten).
- Nachschlagen: `references/demo-design.md` (vor der ersten Demo lesen), `references/ansprache.md`
  (Texte, Recht, Laufzettel), `references/angebot.md` (Pakete, Preise, Pflichten).

## Ablauf

### 1. Gebiet und Rohdaten
Kläre Stadt/Viertel und Ziel (wie viele Leads, für wann, wer geht hin). Unklares nicht erfragen,
wenn eine vernünftige Annahme reicht (z. B. Altstadt/Innenstadt). Dann:

```
python <skill>/scripts/fetch_osm.py --bbox S,W,N,O --out osm.json
python <skill>/scripts/audit.py osm.json --out audit
```

Bbox-Faustwert für eine Altstadt: ca. ±0,005° Breite, ±0,008° Länge um das Zentrum.
Google Maps nicht scrapen (Nutzungsbedingungen, Sperren). OSM ist die Quelle, Google Maps dient nur zum
Ansehen einzelner Läden.

### 2. Kandidaten wählen

**Sperrgebiete:** Läden in `sperrgebiete.json` (Repo-Wurzel) gehören einem anderen Team. Nie dort scannen, beim Dashboard immer `--sperrgebiete sperrgebiete.json` mitgeben.

Aus `audit.json` die 10–15 vielversprechendsten nehmen. Kaufwahrscheinlichkeit vor Score:
- **Höchste Chancen, nach Wert sortiert:** Catering (ein Auftrag bezahlt die Website) > Sitzrestaurant mit Reservierung/Brunch/Gruppen > Friseur/Beauty mit Online-Termin > Imbiss (kleiner Preis, aber schnelle Entscheidung, wenn das Problem greifbar ist, z. B. tote Domain). Imbisse leben oft von Laufkundschaft und Lieferportalen, deshalb das kleine Paket anbieten.
- **Gut:** inhabergeführt, erfolgreich (viele Bewertungen, Traditionshaus), sichtbares Problem
  (Seite tot, Flash, leere Speisekarte, abgeschaltete Domain, keine eigene Seite trotz 700 Bewertungen).
- **Schlecht:** Ketten und Franchises. Seiten, die gepflegt werden (aktuelle Preise) und nur einen
  Kleinfehler haben (→ höchstens kleiner Reparaturauftrag). Ärztliche Werbung (Heilmittelwerbegesetz).
  Läden, die womöglich geschlossen sind.
- Läden **ohne** Website: nur, wenn sie aktiv sind (Bewertungen, Portale) und eine Website wirklich hilft.


**Top-Lead-Kriterien (alle müssen stimmen):**
1. Keine oder schlechte Website, am Screenshot belegt.
2. Inhabergeführt: Das Impressum nennt eine Person bzw. eine kleine GmbH mit dem Inhaber als Geschäftsführer.
3. Keine Kette, kein Franchise, keine Filiale.
4. Läuft und ist aktiv: offen, aktuelle Bewertungen, mindestens 20.
5. Branche ohne Werbeverbot und mit eigener CI-Hoheit, also keine Ärzte, Apotheken, Behörden, Banken oder Versicherungsagenturen.
6. Kein Konflikt mit laufenden Kunden.

`build_leadboard.py` filtert Ketten und diese Branchen automatisch, `--bekannt bekannt.txt` schließt schon bearbeitete Läden aus. Inhaber stehen auf jeder Karte (Felder `inhaber`, `inhaber_quelle`, `inhabergefuehrt`, `bewertungen` in `pruefung.json`). Inhaber nie raten: Quelle ist das Impressum, das Google-Profil, Instagram oder „vor Ort erfragen“.

### 3. Verifizieren (das Wichtigste)
```
python <skill>/scripts/sichten.py --out img slug=url slug2=url2 ...
```
`kontaktbogen.png` ansehen, dann die besten Kandidaten **einzeln in voller Größe** (PC und Handy).
Prüfe jeden Befund des Audits am Bild:

| Befund | Wie prüfen | Heute passiert |
|---|---|---|
| Kaputte Umlaute | nur am Browser-Screenshot, nie aus Python-Text | falscher Alarm bei morph (Dekodierfehler) |
| Kein HTTPS | `curl -sI https://domain` UND Screenshot | morph und Haircouture hatten HTTPS, nur keine Weiterleitung |
| Nicht mobil | Handy-Screenshot: winzig verkleinert oder nur Menü? | |
| Seite tot | Screenshot zeigt Hoster-Meldung/Fehler | Leonardo, The East (fremde WordPress-Seite) |
| Flash | Quelltext `.swf`, Screenshot „Couldn't load plugin.“ | Star Coffee: stärkstes Argument überhaupt |
| Laden geschlossen? | WebSearch „<Name> <Stadt>“ (Branchenbuch, Öffnungszeiten) | |

Dann mit `peek.py` Inhaber (Impressum), Telefon, Geschäfts-E-Mail, Öffnungszeiten, echte Gerichte/Preise
und Geschichte sammeln. Echte Details wie „Haus von 1602“, „seit 1987“ oder „Preise von 2013“ sind Gold
für Demo und Kritik.

**Nur bestätigte Befunde kommen in die Mappe.** Was du korrigierst, sag dem Nutzer offen
(„3 Behauptungen gestrichen, weil falsch“). Das schafft Vertrauen.

**Bei vielen Leads Subagenten einsetzen** (günstiges Modell, z. B. Haiku, im Hintergrund, ca. 30 Läden je Agent):
Gib ein exaktes JSON-Schema vor und definiere jedes Feld eindeutig. Heute haben mehrere Agenten
„verdict: good“ als „guter Lead“ statt „gute Website“ gelesen. Besser getrennte Felder: `status`
(open/closed/unknown), `eigene_website` (URL oder null), `website_qualitaet`, `ist_kette`.
Ihre Ergebnisse sind Hinweise und keine Fakten: Stichproben selbst prüfen, Widersprüche verwerfen.

### 4. Demo pro Laden
Erst `references/demo-design.md` und die Beispiele in `assets/baukasten/kunden/` lesen. Dann pro Laden eine
eigenständige HTML-Datei `showcase-<gebiet>/<slug>.html`: Konzept aus dem Laden, 4 Farben, 2 Schriften,
Name groß, Handy zuerst, echte Daten, Platzhalter für Unbekanntes, Entwurfsbalken mit Absender, `noindex`.
Nach dem Schreiben auf erfundene Zusagen und Statistiken durchsehen und streichen.
Eine Übersicht `index.html` mit allen Demos in Handy-Rahmen hilft beim Zeigen.

### 5. Pitch-Mappen
Kundendatei nach `assets/kunden_beispiel.py` schreiben (ABSENDER, Gebietsfelder, pro Laden: Probleme,
Kritik-Pins mit Koordinaten am *echten* Screenshot, Website-Check mit ✓/✗, Konzept, Farben, Schriften,
Entscheidungen, Paket aus `references/angebot.md`, Was-ich-brauche). Dann:

```
python <skill>/scripts/shots.py --kunden kunden.py --demo-base http://localhost:8765/showcase-<gebiet>/ --out mappen/img
python <skill>/scripts/build_mappen.py --kunden kunden.py --out mappen --vorschau
```

Die Mappe hat 5 Seiten:
1. **Website-Check (Aufhänger):** großer Screenshot von heute mit roten, nummerierten Pins, Handy von heute, ✓/✗-Liste mit „x von 5“, „Das lässt sich in 7 Tagen ändern. Umblättern →“. Ohne Website: nachgestellte, neutral gestaltete Suchansicht, ausdrücklich als nachgestellt beschriftet (kein Google-Logo). Domain tot (löst nicht auf, `python -c "import socket;socket.gethostbyname('domain')"` scheitert): `vorher_art="fehler"` mit `fehler={"domain": …}` → nachgestellte Fehlerseite. Das ist ein sehr starker Aufhänger: Den Inhaber die eigene Adresse auf seinem Handy aufrufen lassen.
2. **Der Entwurf:** PC- und Handy-Ansicht, 3 Begründungen
3. **Gedanken zum Design:** Idee, Farben mit Namen, Schriftmuster mit Ladennamen, Begründungen
4. **Auf dem Handy:** die komplette neue Seite, Bildschirm für Bildschirm
5. **Angebot:** Paket, Betreuung, Monatsmodell, Eröffnungsangebot ohne Zahl, Was-ich-brauche, 4 Schritte, Kontakt („Auf einen Kaffee?“). Will der Nutzer einen Angebotspreis: `angebot={"preis": "690 €", "text": "Einführungspreis, gültig bis <Datum in 2 Wochen>"}`. Der Normalpreis wird durchgestrichen, statt „Eröffnungsangebot“ steht dann die Zahlungsweise da. Vorschlag: etwa 20–25 % unter Normalpreis, echte Frist.

**Prüfen:** Die `vorschau-*.png` von mindestens Seite 1, 2 und 4 einer Mappe ansehen und auf Folgendes achten:
- Pins verdecken das, worauf sie zeigen? Dann Punkt neben das Ziel legen.
- Adresszeile „Nicht sicher“ bei einer https-Seite?
- Abgeschnittener Text, Fußzeile außerhalb der Seite?
- Umbrochener Name im Kontaktblock?

Ein Korrekturdurchgang, dann neu bauen.

### 6. Ansprache und Laufzettel
Nach `references/ansprache.md`: Kontaktliste (Prio, Inhaber mit Quelle, Telefon, bester Weg/Uhrzeit,
Aufhänger) und für einen Besuchstag ein Laufzettel in Laufreihenfolge mit Öffnungszeiten. Ungeprüfte
Öffnungszeiten offen benennen. Die §-7-UWG-Regel immer mitliefern: **keine Werbe-E-Mail ohne vorheriges Ja.**


### 7. Übergabe

Nach einer Zusage gilt `docs/ablauf.md` (Kickoff, Umsetzung, Livegang, Übergabeblatt `vorlagen/Uebergabe-Kunde.html`, Upsell).
**Mappen ohne Absender:** `ABSENDER` in der Kundendatei leer lassen, dann entfallen Name und Nummer.


Nach einer Zusage gilt `notizen/Standard-Ablauf-Kunde.md` (Kickoff, Umsetzung, Livegang, Übergabeblatt `vorlagen/Uebergabe-Kunde.html`, Upsell-Katalog).

**Mappen ohne Absender:** In der Kundendatei `ABSENDER = {"name": "", "telefon": "", "zusatz": ""}` lassen, dann entfallen Name und Nummer in der Mappe (z. B. wenn der andere Partner sie zeigt).

- PDFs und Laufzettel mit `SendUserFile` schicken (display: attach).
- **Demos und Mappen mit echten Firmennamen nicht als öffentliches Artifact veröffentlichen.** Sie bleiben
  lokale Dateien, der Nutzer zeigt sie selbst. Neutrale Werkzeuge (Lead-Board, Angebotsmappe ohne
  Kundennamen) dürfen Artifacts sein.
- Abschluss in wenigen Zeilen: Tabelle der Leads (Laden, Ansprechpartner, Aufhänger), was gestrichen oder
  korrigiert wurde, was noch fehlt (Telefon, Inhaber, Zeiten), nächster sinnvoller Schritt.
- Liegt die Arbeit in einem temporären Ordner, anbieten, sie in einen dauerhaften Ordner zu verschieben.

## Dashboard (Lead-Board)

Ein lokales Dashboard in **einer HTML-Datei**: Pipeline-Leiste (Neu, Hot, Warm, Kalt, Kein Lead, Kontaktiert, Termin,
Gewonnen), Suche, Filter nach Liste/Branche, Sortierung nach Score oder Straße (Laufroute), Detailkarte mit Problem,
Pitch-Idee, Telefon, Google-Maps-Link und Notizfeld, Tastatur (J/K blättern, 1–7 einstufen, N Notiz, / Suche),
CSV-Export und Backup. Einstufungen und Notizen bleiben im Browser (localStorage). Kontaktdaten Dritter bleiben lokal,
die Datei kommt **nicht** ins Git-Repo.

Ablauf:
1. Nach dem Sichten (Schritt 3) die bestätigten Befunde als `pruefung.json` schreiben (Schema im Kopf von
   `scripts/build_leadboard.py`, Beispiel `assets/leadboard/pruefung_beispiel.json`). Nur belegte Angaben eintragen,
   Unbekanntes leer lassen. `status` ist `open`, `closed` oder `unknown`.
2. Bauen:
   ```
   python <skill>/scripts/build_leadboard.py --audit audit.json --pruefung pruefung.json --stadt <Stadt> --untertitel "Altstadt" --out leadboard.html
   ```
3. Zum Anzeigen lokal öffnen (Datei im Browser) oder `python -m http.server 8765` im Ordner. Dem Nutzer sagen, wo die Datei liegt.
4. Wiederholen nach neuen Prüfungen: Die Einstufungen bleiben erhalten (Schlüssel pro Stadt, Lead-ID aus Name und Adresse).

Läden ohne Website laut OSM kommen nur ins Board, wenn sie in `pruefung.json` als offen bestätigt sind, sonst ist das
Rauschen (OSM kennt die Website oft nur nicht).

## Website-Standard (gilt für jede Live-Seite)

Jede Seite, die an einen Kunden geht, erfüllt **`references/website-standard.md`**: saubere Architektur (eine Quelle für Inhalte, Partials, Design-Tokens, Komponenten, Progressive Enhancement, README für den Nachfolger) und lokales SEO (Titel/Description pro Seite, eine H1, JSON-LD LocalBusiness, NAP identisch mit Google-Profil, Sitemap, robots, schnelle Bilder, Lighthouse ≥ 90).
Damit sie auch **hochwertig** aussieht, gilt **`references/design-qualitaet.md`**: Design-System aus Tokens, Typografie, Weißraum und Rhythmus, Komponenten mit allen Zuständen, Profi-Check vor jeder Vorschau. Kunden-Fragebogen: `vorlagen/Projekt-Fragebogen.html`.
Prüfen: `python <skill>/scripts/website_check.py <ordner>`, vor dem Livegang mit `--live`. **Kein Livegang mit ✗.**
Design-Änderungen an einer bestehenden Seite immer mit Vorher/Nachher belegen:
```
python <skill>/scripts/vergleich.py --sichern <kunde>/dist          # vor der Änderung
python <skill>/scripts/vergleich.py <gesicherter-ordner> <kunde>/dist [--abschnitt index:#besuch]
```
Die Bilder landen in `<kunde>/vergleich/<datum-uhrzeit>/` (lokal, nicht veröffentlichen) und gehen so an den Nutzer bzw. Kunden.

## Weitere Bausteine (bei Bedarf)

- **Lead-Board** (Dashboard, eine lokale HTML-Datei): siehe Abschnitt „Dashboard“ unten.
- **Echte Live-Seite** nach Zusage: `assets/baukasten/` (JSON pro Kunde → `build.py` → statische Seite mit
  lokalen Schriften, Impressum/Datenschutz mit [FEHLT]-Markierung). Siehe dortige README.
- **Telefonskript / Hormozi-Pitch, Preise und Pakete:** `references/ansprache.md` und `references/angebot.md`.
