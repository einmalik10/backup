# Website-Standard: SEO und saubere Architektur (gilt für jede Live-Seite)

Jede Website, die an einen Kunden geht, erfüllt diesen Standard. Er gilt nicht für schnelle Demos und Mappen, aber für alles, was online geht.
Prüfen mit: `python <skill>/scripts/website_check.py <ordner-der-seite>`. **Livegang erst, wenn keine Fehler (✗) mehr da sind.** Warnungen (!) bewusst entscheiden.

## 1. Architektur (Clean Architecture für kleine statische Seiten)

**Grundidee:** Inhalt, Aussehen und Verhalten sind getrennt. Eine Änderung (neue Öffnungszeit, neuer Preis) passiert an **genau einer** Stelle.

```
<kunde>/
├── inhalt.json            ← einzige Quelle für Name, Adresse, Telefon, Zeiten, Karte, Leistungen, Texte
├── templates/             ← Seiten als Jinja-Vorlagen, gemeinsame Teile als Partials
│   ├── _layout.html       (Kopf, Navigation, Fuß, JSON-LD einmal zentral)
│   ├── index.html, <seite>.html
│   └── impressum.html, datenschutz.html, 404.html
├── assets/
│   ├── css/style.css      ← Reihenfolge: Tokens → Base → Layout → Komponenten → Seiten → Utilities
│   ├── js/                ← klein, ein Zweck pro Datei (z. B. formular.js), kein Inline-JS außer JSON-LD
│   ├── img/               ← WebP, je Bild 2 Größen (-800, -1600), sprechende Dateinamen
│   └── fonts/             ← woff2 lokal (keine Google-Fonts-Server, DSGVO)
├── server/anfrage.php     ← falls Formular: Konfiguration oben, Prüfung serverseitig, Spam-Falle
├── build.py               ← rendert templates + inhalt.json → dist/
├── dist/                  ← das, was hochgeladen wird (nie von Hand ändern)
└── README.md              ← für den Kunden/Nachfolger: wo was steht, wie man ändert und neu baut
```

**Regeln**
- **Eine Quelle:** Name, Adresse, Telefon und Zeiten stehen nur in `inhalt.json`. Kopf, Fuß, Kontaktbereich, JSON-LD und Impressum lesen daraus, deshalb stimmen sie immer überein (wichtig für Google, „NAP-Konsistenz“).
- **Keine Kopien:** Kopf und Fuß als Partial, nicht in jede Seite kopiert.
- **Design-Tokens:** Farben, Schriften, Abstände und Radien als CSS-Variablen in `:root`. Keine Farbwerte verstreut im CSS, kein `!important`.
- **Komponenten:** wiederverwendbare Klassen (`.btn`, `.card`, `.section`), mit einheitlichem Präfix oder BEM-artiger Benennung. Mobile first, `min-width`-Media-Queries.
- **Progressive Enhancement:** Die Seite funktioniert ohne JavaScript (Formular schickt trotzdem ab, Inhalte sind sichtbar). JS verbessert nur.
- **Keine Abhängigkeiten zur Laufzeit:** keine CDNs, Tracker oder Frameworks, wenn nicht nötig. Dann braucht man keinen Cookie-Banner und es gibt keine Updates.
- **Formular-Logik getrennt:** `anfrage.php` mit Konfiguration ganz oben (Empfänger, Absender), Felder serverseitig prüfen, Honeypot, Weiterleitung auf `danke.html` oder `fehler.html`.
- **Übergabefähig:** `README.md` im Kundenordner. Jemand anderes muss die Seite in 10 Minuten verstehen und ändern können.
- Kleine Onepager dürfen ohne `build.py` auskommen, aber dann gilt trotzdem: Tokens, Komponenten, keine Inhalte doppelt pflegen.

## 2. SEO (lokal)

**Pro Seite**
- Eigener `<title>` (50–60 Zeichen): `Leistung/Branche + Stadt · Name`, z. B. „Kfz-Werkstatt Musterstadt · Autohaus Muster“.
- Eigene `<meta name="description">` (120–160 Zeichen), mit Nutzen und Handlungsaufforderung.
- Genau **eine `<h1>`**, darunter sinnvolle `<h2>`/`<h3>`. Überschriften enthalten natürlich Branche und Ort.
- `<link rel="canonical">` mit der Hauptadresse (`https://www.…`).
- `<html lang="de">`. Bei zweisprachigen Seiten `hreflang` für beide Sprachen.
- Open-Graph-Tags (`og:title`, `og:description`, `og:image`) für schöne Vorschauen in WhatsApp und Facebook.
- Alle Bilder mit aussagekräftigem `alt`, dazu `width` und `height` (verhindert Springen), unterhalb des ersten Bildschirms `loading="lazy"`.

**Inhalt**
- Karte, Preise und Leistungen als **Text in HTML**, nie nur als Bild oder PDF.
- Branche und Stadt (und das Viertel) kommen natürlich im Text vor, nicht gestopft.
- Interne Links zwischen den Seiten (z. B. von Start zu Speisekarte und Anfrage).
- Echte, belegte Inhalte: Google wertet dünne und kopierte Texte ab.

**Strukturierte Daten (JSON-LD, zentral im Layout)**
- Passender Typ: `Restaurant`, `AutoRepair`, `AutoDealer`, `HairSalon`, `BeautySalon`, `Bakery`, `Store` … (sonst `LocalBusiness`).
- Pflicht: `name`, `address` (PostalAddress), `telephone`, `url`, `image`, `openingHoursSpecification`. Wenn vorhanden: `menu`, `priceRange`, `servesCuisine`, `geo`, `sameAs` (Instagram, Facebook).
- Keine erfundenen Bewertungen im Markup.

**Technik**
- `robots.txt` mit Verweis auf `sitemap.xml`. In der Sitemap stehen alle öffentlichen Seiten (ohne danke/fehler).
- `404.html`. HTTPS mit Weiterleitung, eine Hauptadresse (`www` oder ohne), alte Domains per 301 auf die neue.
- **Schnell:** Bilder WebP und meist unter 200 KB, wichtigste Schrift per `preload`, kein Render-Blocker von außen. Ziel: Lighthouse ≥ 90 in Performance, SEO, Barrierefreiheit und Best Practices; LCP < 2,5 s, CLS < 0,1.
- **Barrierefreiheit hilft SEO:** Kontrast, sichtbarer Fokus, `label` an jedem Formularfeld, Knöpfe sind Links oder Buttons.
- Vor dem Livegang `noindex` entfernen. Danach: Google Search Console einrichten, Sitemap einreichen.

**Google-Unternehmensprofil** (oft wichtiger als die Website selbst)
- Website- und Menü-Link auf die neue Seite, Kategorie, Zeiten, Fotos, Leistungen. Name, Adresse und Telefon genau wie auf der Website.

## 3. Abnahme (vor jedem Livegang)
1. `website_check.py` ohne ✗.
2. Lighthouse (Chrome DevTools) für Start- und Hauptseite am Handy: alle vier Werte ≥ 90 oder Abweichung begründet.
3. Links, Formular (Testanfrage kommt an), Anrufen und Route am echten Handy getestet.
4. `README.md` im Kundenordner aktuell.
