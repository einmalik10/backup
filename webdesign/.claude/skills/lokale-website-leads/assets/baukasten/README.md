# Demo-Baukasten: Websites für lokale Läden

Drei Branchen-Vorlagen (Beauty, Gastro, Praxis). Pro Laden eine JSON-Datei → fertige Website.

## Einmalig

```
pip install jinja2
```

## Neue Demo in 30–60 Minuten

1. Passende Beispieldatei kopieren: `kunden/beispiel-beauty.json` → `kunden/salon-xy.json`
2. `slug` ändern (z. B. `salon-xy`), dann Name, Adresse, Telefon, Öffnungszeiten und Preise
   aus dem Google-Profil, von Instagram oder der Speisekarte übernehmen.
3. `farbe` an Logo oder Ladenschild anpassen (Hex-Wert, z. B. `#6d3b5e`).
4. Fotos (optional) in `kunden/salon-xy/` ablegen und in `"bilder"` eintragen:
   `"bilder": {"hero": "hero.jpg", "galerie": ["1.jpg", "2.jpg", "3.jpg"]}`
5. Bauen: `python build.py kunden/salon-xy.json`
6. Ansehen: `out/salon-xy/index.html` im Browser öffnen. Zum Zeigen auf dem Handy
   den Ordner `out/salon-xy` per Drag-and-drop auf Netlify Drop oder Cloudflare Pages hochladen
   (kostenloser Link, `demo: true` sorgt dafür, dass Google die Demo nicht indexiert).

## Wichtige Felder

| Feld | Wirkung |
|---|---|
| `buchung_url` / `reservierung_url` / `termin_url` | Link zu Treatwell, Planity, Doctolib, OpenTable … Leer = Knopf ruft an. |
| `whatsapp` | Nummer, falls Buchung per WhatsApp laufen soll (nur wenn kein Buchungslink). |
| `oeffnungszeiten` | `"mo": ["09:00-18:00"]`, Mittagspause: `["08:00-12:00", "14:00-18:00"]`. Fehlender Tag = geschlossen. |
| `hinweis` | Balken oben, z. B. „Betriebsurlaub 20.–27. Dezember“. |
| `bewertung` | Nur echte Werte aus Google: `{"sterne": 4.8, "anzahl": 212, "url": "…"}` |
| `demo` | `true` = Entwurfs-Hinweis oben + nicht in Google. Vor dem Livegang auf `false`. |

## Vor dem Livegang (Pflicht)

- [ ] Kunde hat zugestimmt, dass seine Fotos genutzt werden (eigene Fotos, nicht von Fremden)
- [ ] Impressum vollständig: keine gelben **[FEHLT: …]** mehr auf `impressum.html`
- [ ] Datenschutzerklärung aus einem Generator in `datenschutz_html` eintragen
- [ ] `demo` auf `false`, `domain` eintragen
- [ ] Alle Links (Buchung, Instagram, Lieferdienste) einmal angeklickt
- [ ] Auf dem Handy getestet: Anrufen, Route, Buchen
