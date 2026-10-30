# MI Visuals Website

- **Status:** aktiv
- **Ziel (messbar):** Eigene Agentur-Website live, die Anfragen für Branding, Film und Websites bringt
- **Deadline:**
- **Bringt Geld?** indirekt, über Kundenanfragen
- **Ordner:** `C:\Users\Malik\Desktop\mi-visuals\mi-visuals`
- **GitHub:** https://github.com/einmalik10/Mi-Visuals
- **Lokal starten:** `Seite starten.bat` → http://localhost:8000
- Gehört zu [[Webdesign]]

## Nächste Schritte
- [ ] Zusagen auf `webseiten.html` prüfen („Und wenn etwas schiefgeht?“, Festpreis), bevor die Seite online geht
- [ ] Pflichtangaben eintragen: Impressum (Straße, PLZ/Ort) und Datenschutz (Hosting-Anbieter, Platzhalter) – ohne das nicht online gehen
- [ ] Formspree-ID im Kontaktformular eintragen (bis dahin öffnet das Formular eine fertige E-Mail)
- [ ] Echten Screenshot für BC Automobile einsetzen
- [ ] Für echtes 4K-Showreel das Kamera-Original des Salam-Films besorgen (nicht per WhatsApp)
- [ ] Hosting wählen (z. B. GitHub Pages) und Domain mivisuals.de verbinden

## Notizen
- 2026-10-19 · Region auf der Seite nur „Stuttgart“ (Malik will Sindelfingen/Böblingen nicht mehr nennen).
- 2026-10-19 · Look: Luxus-Sport (breite Grotesk + kursive Serife, Metall-Gold, scharfe Kanten). Unterseite `webseiten.html` nach Vorbild dd-muc.de mit Live-Demos und Farbschalter.
- 2026-10-19 · Rot als Hausfarbe ausprobiert und wieder verworfen → Hausfarbe bleibt Gold (#FFB000).
- 2026-10-19 · Referenzen: Loretto Markt Salam und Istanbul Tübingen als Live-Projekte; Showreel ist ein 28-s-Schnitt aus dem Salam-Film.
- 2026-10-20 · Projektkarte BC Automobile ersetzt durch „Autohaus · Website-Konzept“ (Screenshot der Vorlage-Autohaus, ohne Link). Reservierungs-Demo auf `webseiten.html`: Datum ab heute, Personen 1/3/5/8+. ZIP `fuer-netcup.zip` auf dem Desktop (index, impressum, datenschutz, assets). Achtung: `webseiten.html` ist nicht in der ZIP, wird aber von index.html verlinkt.

## Gelernt
- Siehe [[Learnings]] (Einträge vom 2026-10-19: iframe-Sperre, Browser-Cache, Ruckeln durch teure Effekte).
- 2026-10-20 · Autohaus-Karte scrollt jetzt beim Drüberfahren durch die ganze Vorlage (Bild 1200×6963, `project--long`, auf dem Handy automatisch).
- 2026-10-20 · Kontaktformular in 4 Schritten: Worum geht’s (Pflicht) → Wunschtermin + Budget → Name + E-Mail → Nachricht + Datenschutz → Anfrage senden. Telefon und Unternehmen sind dabei rausgefallen (Sicherung in `Sicherung-2026-10-20/vor-kontakt-schritte`).
- 2026-10-20 · Reservierungs-Demo: Personen 1/2/3/4/5+; vergangene Uhrzeiten heute live durchgestrichen (Uhr des Besuchers, alle 30 s), gewählte Zeit springt auf die nächste freie.
- 2026-10-20 · Ruckeln am PC behoben (Lichtschleier ohne Drehen, Demo-Karten ohne Blur): Startseite 52 % → 3 % zu langsame Bilder, Websites-Seite 85 % → 6 %. Upload-ZIP jetzt komplett (7 Dateien + assets). Impressum/Datenschutz haben noch Platzhalter (Adresse, Hosting).
- 2026-10-20 · Live auf mivisuals.de (netcup, httpdocs), Let's-Encrypt-Zertifikat für mit und ohne www, HTTP→HTTPS an. Im eigenen WLAN blockiert ein Webfilter die Domain, übers Handy klappt es. Offen: Impressum/Datenschutz-Platzhalter.
- 2026-10-20 · Stand auf GitHub gepusht (einmalik10/Mi-Visuals, Commit a1456ac). Im lokalen Klon `Desktop/mi-visuals/mi-visuals` liegen noch alte, nicht committete Änderungen von 16:35 → klären, ob die weg können.
- 2026-10-21 · Showreel (Salam-Film) wieder oben im Hero statt Logo-Platzhalter. Impressum/Datenschutz: PLZ/Ort, Hoster netcup und Stand eingetragen; offen: Straße + Hausnummer, USt-Hinweis, Log-Speicherdauer, Formspree-Abschnitt (Formular nutzt aktuell E-Mail statt Formspree).
- 2026-10-22 · Salam-Film: einzige Quelle auf dem PC ist die WhatsApp-Version mit 1024×576 (Desktop/Loretto Markt Salam). Das Showreel (1920×1080) ist daraus schon hochgerechnet. Für Ultra HD braucht es die Original-Datei von Kamera/Handy/Schnittprogramm.
- 2026-10-22 · Neue Projektkarte „Bassam the Butcher · Onlineshop“ (Link shop.bassamthebutcher.com, Bild 1200×3000) zwischen Istanbul und Autohaus. Update-ZIP auf dem Desktop: index, impressum, datenschutz + Bild.
- 2026-10-22 · Laufband klickbar: Begriff → Formular mit passender Leistung angehakt, direkt Schritt 2 („Ausgewählt: … · ändern“). Neue Auswahl „Fotografie“ im Formular. Update-ZIP: 5 HTML + style.css + main.js + Bassam-Bild.
