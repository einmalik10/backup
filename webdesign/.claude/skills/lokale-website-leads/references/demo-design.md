# Demo-Websites, die überzeugen

Eine Demo ist kein Template mit ausgetauschtem Namen. Der Inhaber muss beim ersten Blick denken:
„Das ist *mein* Laden.“ Beispiele für Kundendaten liegen in `assets/baukasten/kunden/`. Echte Demos von Läden gehören nicht ins Repo
(Markenauftritt fremder Firmen), sie werden pro Laden lokal gebaut.

## 1. Das Konzept kommt aus dem Laden selbst

Suche nach dem *einen* Detail, das nur dieser Laden hat, und baue die Seite darum:

| Quelle | Beispiel von heute | Ergebnis |
|---|---|---|
| **Name** | „First Class“ | Bordkarte, Abflugtafel als Preisliste, „Check-in“ statt „Buchen“ |
| | „morph“ (= Verwandlung) | sich langsam verformende Farbfläche, „change your hair.“ |
| | „Leonardo“ | Rötel-Skizze wie da Vincis Proportionsstudien |
| | „Antik Barber“ | Apotheker-Etikett, Siegel mit den Sternen, Barber-Pole |
| **Schild / Fassade** | Café Prag: rotes Hängeschild | Schild als animiertes Markenzeichen oben |
| | Krumme Brücke: grüner Fraktur-Schriftzug | Name riesig in Fraktur („Kulturgut“) |
| **Geschichte** | Haus von 1602, das „B“ über der Tür | eigener Abschnitt, Zahlen-Kacheln |
| **Stärkstes Argument** | Star Coffee hat bis 21 Uhr offen | drehender Sticker „offen bis 21 Uhr“, Uhr „21:00“ |
| | 742 Bewertungen, 4,69 ★ | Bewertung direkt unter der Überschrift |
| **Eigene Begriffe** | Little India: nummerierte Karte | Nummern bleiben („die 19“) |

Woher: das Impressum, die „über uns“-Seite, Fotos der Fassade (Bildersuche nur **ansehen**,
nie übernehmen), Bewertungsportale, Presseartikel. Wenn der Name, das Schild oder die Geschichte etwas
hergeben, ist das Konzept fast immer besser als jede Branchen-Vorlage.

**Der Name des Ladens ist heilig.** Er gehört groß und gut sichtbar in den Kopfbereich, besonders bei
Traditionsbetrieben. Der Nutzer hat das ausdrücklich verlangt: „ist schließlich Kulturgut“.

## 2. Gestaltung

- **Farben:** 4 Töne, aus dem Laden abgeleitet (Logo, Schild, Markise, Produkt). Mit Namen benennen
  („Schildrot“, „Ammerkanal“). Diese Namen landen in der Mappe.
- **Schriften:** 2 Google Fonts. Eine charakterstarke für Überschriften, eine ruhige für Text.
  Nicht Inter, Roboto oder Arial. Für die Demo dürfen Google Fonts per Link geladen werden. Für die
  **echte** Seite später lokal einbinden (DSGVO), siehe Baukasten.
- **Aufbau (Handy zuerst):** Kopf mit Name und Haupt-Knopf → Hero mit Name/Claim, 1 Satz, 2 Knöpfe →
  Besonderheiten (3 Kacheln) → Karte/Preise/Leistungen → Geschichte/Extra → Besuch (Adresse,
  Zeiten-Tabelle, Anrufen, Route) → Fußzeile mit Impressum/Datenschutz.
- **Pflicht in jeder Demo:**
  - `<meta name="robots" content="noindex">`
  - Ein Balken oben: „Entwurf für <Laden> · unverbindlich von <Absender>“
  - `tel:`-Links mit der echten Nummer
  - Google-Maps-Link als **Link**, nicht eingebettet
  - Bilder als farbige Platzhalter mit Beschriftung („Foto: Gastraum“)
- Sprungmarken (`id="karte"`, `id="besuch"`, …) für die Navigation setzen.
- Klassennamen nicht doppelt vergeben. Heute hat `.g` (Speisekarten-Zeile) einen Knopf `.knopf.g`
  zerschossen.
- Bewegung sparsam: ein Effekt pro Seite (schwingendes Schild, drehender Sticker, Dampf) und
  `prefers-reduced-motion` respektieren.
- Die Seite muss bei 390 px Breite funktionieren: kein Überlauf, Titel mit `clamp()`. Nach dem Bauen
  einmal auf Handy-Breite ansehen.

## 3. Inhalte: nur Echtes, sonst Platzhalter

- Echt übernehmen: Name, Adresse, Telefon, Öffnungszeiten, Gerichte, Preise, Geschichte, Team, und
  zwar von der eigenen Seite des Ladens oder aus seriösen Einträgen.
- Was du nicht weißt, wird `[Platzhalter]` oder als „Beispiel“ gekennzeichnet
  („Beispielpreise im Entwurf · werden durch Ihre ersetzt“).
- **Nicht erfinden:** Zusagen („in 15 Minuten abholen“), Leistungen („Torten auf Bestellung“,
  „Hafermilch ohne Aufpreis“), Statistiken („drei Viertel der Suchen …“), Kundenzitate,
  Inhaber-Titel. Heute wurden alle diese Beispiele noch vor der Abgabe gestrichen.
- Bewertungszahlen nur mit Quelle (z. B. werkenntdenbesten.de) und im Gespräch als Portal-Wert nennen.
- Keine Funktionen versprechen, die die Demo nicht hat. Statt „Sie pflegen das selbst in 30 Sekunden“:
  „Schicken Sie mir ein Foto, ich aktualisiere es am selben Tag.“

## 4. Ablage

Demos als einzelne HTML-Dateien in einen Ordner, z. B. `showcase-<stadt>/<slug>.html`. Dazu eine
Übersicht `index.html` mit allen Demos in Handy-Rahmen (iframes, Skalierung 0.718 bei 390 px)
mit „Heute: … / Neu: …“ pro Laden.

**Nie als öffentliches Artifact oder auf öffentlichem Hosting veröffentlichen:** Demos tragen Namen und
Markenauftritt echter Firmen. Zum Zeigen lokal öffnen, oder per Passwort-Link nur für den Inhaber.
