# Design-Qualität: vom „ordentlich“ zum „wie von einer Agentur“

Der Website-Standard sorgt dafür, dass eine Seite **richtig** ist (SEO, Architektur). Diese Datei sorgt dafür, dass sie **hochwertig aussieht**. Gilt für jede echte Website und jedes Dokument, das ein Kunde in die Hand bekommt (Fragebogen, Angebot, Übergabe).

Der Unterschied zwischen Amateur und Profi liegt selten in einer großen Idee, sondern in hundert kleinen Entscheidungen, die alle konsequent gleich getroffen werden. Darum: **System statt Einzelfall.**

## 1. Das System zuerst (vor der ersten Seite)

Lege in `:root` fest und benutze danach **nur noch diese Werte**:

| Token | Regel | Typischer Fehler |
|---|---|---|
| **Abstände** | 8er-Raster: 4, 8, 12, 16, 24, 32, 48, 72, 112 px | 15 px hier, 22 px dort, 37 px da |
| **Schriftgrößen** | Feste Stufen, Verhältnis ca. 1,25: 14 · 16/17 · 20 · 25 · 32 · 40 · 52 · 64+; Überschriften mit `clamp()` | 7 verschiedene Größen, die fast gleich sind |
| **Farben** | 1 Tinte, 2–3 Grautöne aus der Tinte, 1 Akzent (+ dunkle Stufe für Hover), 1 Papier | Reines `#000` auf `#fff`, Akzent überall |
| **Radien** | 2–3 Werte (z. B. 8 / 14 / 22) und Pillen-Knöpfe, konsequent | jede Karte anders rund |
| **Schatten** | 1–2 weiche, mehrlagige Schatten | harter `box-shadow: 0 0 10px #000` |
| **Bewegung** | 1 Dauer (~200 ms), 1 Kurve (`cubic-bezier(.2,.7,.2,1)`) | jede Animation anders schnell |

## 2. Typografie (der größte Hebel)

- **Zwei Schriften, klare Rollen.** Charakter für Überschriften, ruhig für Text. Ein großer Kontrast in Größe (H1 mindestens 2,5× Fließtext) wirkt sofort teurer.
- **Fließtext 16,5–18 px**, Zeilenhöhe 1,55–1,65, Zeilenlänge **max. 60–70 Zeichen** (`max-width: 60ch`).
- **Überschriften eng:** Zeilenhöhe 1,0–1,15, leicht negatives `letter-spacing` (−0,01 bis −0,02 em) bei großen Größen.
- **Überzeile (Eyebrow)** über Abschnittstiteln: 12 px, Versalien, `letter-spacing: .14–.18em`, Akzentfarbe. Kleine Geste, großer Ordnungseffekt.
- **Echte Typografie:** „Anführungszeichen“, Gedankenstrich –, geschütztes Leerzeichen in „10 Uhr“ und „5 €“, `font-variant-numeric: tabular-nums` in Preislisten und Zeiten.
- **Ein Wort hervorheben** statt ganze Sätze fett: z. B. kursiv in Akzentfarbe im H1.
- Schriften lokal, mit `font-display: swap` und `preload` der Überschriftenschrift.

## 3. Layout und Rhythmus

- **Großzügiger Weißraum** ist das sichtbarste Qualitätsmerkmal. Abschnitte am PC 96–128 px Abstand, am Handy 56–72 px. Lieber zu viel als zu wenig.
- **Ein Raster:** Inhalt max. 1120–1200 px, Text max. 60–70 Zeichen. Alles fluchtet an denselben Kanten.
- **Abwechslung im Takt:** Abschnitte wechseln Hintergrund (Papier → Weiß → Dunkel) oder Aufbau (Text links/Bild rechts → umgekehrt → volle Breite). Nie fünfmal dasselbe Muster.
- **Hierarchie in drei Ebenen:** Was sieht man zuerst (H1 + Bild), was dann (Knopf), was zuletzt (Details). Wenn alles laut ist, ist nichts wichtig.
- **Ein Hauptknopf pro Bildschirm.** Daneben höchstens ein ruhiger Zweitknopf (Umriss).

## 4. Fotos und Bilder

- **Echte Fotos vom Laden schlagen jedes Stockfoto.** Wenn die Fotos schwach sind: Fotoshooting anbieten (Upsell), nicht „irgendwas“ nehmen.
- **Ein Bildstil:** gleiche Farbstimmung, ähnliches Licht. Notfalls alle Bilder leicht gleich behandeln (Wärme, Kontrast), nie Filter mischen.
- **Ausschnitt bewusst:** `object-fit: cover` mit `object-position` gezielt setzen, feste Seitenverhältnisse (4:5 Porträt, 3:2 Szene, 1:1 Produkt).
- Hero: Bild hochwertig und groß oder gar keins. Ein kleines Bild in einer großen Fläche wirkt billig.
- Keine Bilder mit Text darin (Flyer, Screenshots von Karten). Text gehört ins HTML.

## 5. Komponenten mit allen Zuständen

Jeder Knopf, jedes Feld, jede Karte hat **alle Zustände** gestaltet, nicht nur den Normalzustand:

| Zustand | Was gehört dazu |
|---|---|
| Normal | klare Form, Mindesthöhe 44–50 px |
| Hover | leichte Veränderung (dunkler, Schatten, Pfeil rückt 3 px) |
| Fokus (Tastatur) | sichtbarer Ring in Akzentfarbe, `:focus-visible` |
| Aktiv | kurz kleiner (`scale(.98)`) |
| Deaktiviert / Fehler / Erfolg | Farbe plus Text, nie nur Farbe |

Formulare: Label **über** dem Feld (nie nur Platzhalter), Felder ≥ 50 px hoch, 16 px Schrift (sonst zoomt das iPhone), Fehlermeldung direkt am Feld, Auswahl lieber als große Karten oder Chips als als Dropdown.

## 6. Details, die Profis verraten

- Favicon (SVG + PNG), `theme-color`, schönes `og-bild.jpg` 1200×630.
- Telefonnummern als `tel:`, Adresse als Maps-Link, Öffnungszeiten mit „Jetzt geöffnet“.
- Leere Zustände und Fehlerseiten (404) im selben Design.
- Kein Layout-Springen beim Laden (Bildgrößen, Schrift-Fallback mit ähnlicher Breite).
- Fußzeile ist ein echter Abschnitt (Logo, Kontakt, Zeiten, Links), kein grauer Rest.
- Bewegung: **ein** Effekt beim Erscheinen (sanftes Einblenden 10 px von unten), überall gleich, mit `prefers-reduced-motion` aus.
- Ein konsistenter Ton: entweder „du“ oder „Sie“, überall.

## 7. Dokumente für Kunden (Fragebogen, Angebot, Übergabe)

Alles, was der Kunde in die Hand bekommt, ist Teil der Marke und wird **genauso** gestaltet:

- Kein PDF mit 50 Seiten Freitextfeldern. Fragebögen als **`vorlagen/Projekt-Fragebogen.html`**: in Schritten, mit Fortschritt, Auswahlkarten statt leerer Kästen, automatisch gespeichert, am Handy ausfüllbar, Ergebnis als Datei (JSON für Claude) oder PDF.
- Fragen, deren Antwort du schon kennst (aus Shop, Google, Instagram), **vorbefüllen und bestätigen lassen** statt neu fragen: „Im Shop steht 20 € Versand. Stimmt das?“
- Jede Frage braucht einen Grund. Was nicht in die Website einfließt, fliegt raus.
- Tiefe Spezialfragen (Shop, Versand, Beratung) als eigenes, kurzes Kapitel erst **nach** dem Grund-Fragebogen.

## 8. Abnahme: Profi-Check (zusätzlich zu `website_check.py`)

Vor jeder Vorschau beim Kunden ehrlich abhaken. Screenshots am PC (1440 px) und Handy (390 px) ansehen, nicht nur den Code.

- [ ] Alle Abstände, Größen, Farben kommen aus den Tokens (keine Einzelwerte im CSS).
- [ ] H1 mindestens 2,5× so groß wie Fließtext, Textzeilen höchstens ~70 Zeichen.
- [ ] Pro Bildschirm genau ein Hauptknopf.
- [ ] Abschnitte wechseln im Takt (Hintergrund oder Aufbau), nichts wirkt wie Copy-Paste.
- [ ] Alle Fotos echt, scharf, in einem Stil, bewusst zugeschnitten.
- [ ] Hover, Fokus und Aktiv-Zustand an Knöpfen, Links und Feldern sichtbar.
- [ ] Typografie: richtige Anführungszeichen, Gedankenstriche, keine Waisen in Überschriften (`text-wrap: balance`).
- [ ] Favicon, og-Bild, 404 im Design.
- [ ] Handy: Daumen erreicht den Hauptknopf, kein waagrechtes Scrollen, nichts zu klein (< 14 px).
- [ ] **Blinzeltest:** Screenshot verkleinern oder Augen zusammenkneifen. Erkennt man sofort Name, Angebot und Knopf?
- [ ] **Vergleichstest:** neben eine sehr gute Seite derselben Branche legen. Was fehlt noch? Das eine Ding verbessern.
- [ ] **Vorher/Nachher** bei jeder Überarbeitung: `scripts/vergleich.py` (erst `--sichern dist`, nach der Änderung `vergleich.py <sicherung> dist`). Erzeugt ersten Bildschirm und ganze Seite für PC und Handy nebeneinander, Seitenlängen und Überlauf-Prüfung.
