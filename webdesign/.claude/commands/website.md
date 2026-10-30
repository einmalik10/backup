---
description: Nach der Zusage die echte Website bauen (Kickoff, Umsetzung, Livegang)
---
Der Laden „$ARGUMENTS“ hat zugesagt. Arbeite nach `docs/ablauf-kurz.md` (Kickoff, Umsetzung, Livegang), nach `.claude/skills/lokale-website-leads/references/website-standard.md` (richtig) und nach `.claude/skills/lokale-website-leads/references/design-qualitaet.md` (hochwertig).

## 0. Vorab klären (eine Nachricht, gesammelt)
- Liegt der Laden in `sperrgebiete.json`? Dann nur weiter, wenn der Nutzer selbst Inhaber ist oder der Repo-Inhaber zugestimmt hat.
- Frag nach: Material (Logo als PDF/SVG, Fotos, bestehende CI, Social-Profile), Paket/Preis, ob Anfragen per Formular nötig sind, Stil-Wunsch.
- Recherchiere selbst (Google-Profil, Instagram-Bio, Branchenbuch): Adresse, Zeiten, Telefon, Bewertungen, Inhaber, alte Domains. Was nur aus einer KI-Antwort oder einem Portal stammt, bekommt `[PRÜFEN]`.

## 1. Kundennotiz und Kickoff
- **Projekt-Fragebogen:** `vorlagen/Projekt-Fragebogen.html?laden=<Name>` an den Kunden geben (oder beim Kickoff gemeinsam am Tablet ausfüllen). Die zurückgeschickte `fragebogen-<laden>-<datum>.json` nach `arbeit/kunden/<slug>/quelle/` legen und daraus `inhalt.json`, Ton, Stil und Hauptknopf ableiten. Bekanntes nicht neu fragen, sondern zur Bestätigung vorlegen. Spezialfragen (Shop, Versand) nur als kurzes Zusatzkapitel.
- `vorlagen/Kunde.md` → `arbeit/kunden/<Laden>.md` (lokal). Dazu Belege mit Quelle und Datum.
- Kickoff-Liste: Was unterschreiben (Foto-Freigabe aller abgebildeten Personen, AVV mit dem Hoster), was erfragen (Impressumsdaten: Firma, Inhaber laut Register, HR-Nr., USt-IdNr., bei Meisterbetrieb die Kammer), welche Fotos fehlen.

## 2. Gestaltung: bestehende CI übernehmen und vereinen
- Zuerst das Design-System als Tokens festlegen (Abstände 8er-Raster, Schriftstufen, Farben, Radien, Schatten, Bewegung), siehe `design-qualitaet.md` Abschnitt 1. Danach keine Einzelwerte mehr.
- Farben **aus Logo und Laden messen** (Pixel aus dem Logo, Wand, Schild), als Tokens mit Namen und Herkunft. Knopffarben auf Kontrast ≥ 4,5 prüfen und bei Bedarf abdunkeln.
- Logo aus PDF sauber übernehmen (PyMuPDF, freigestellt, ohne weißen Kasten). Mehrere Marken (z. B. Markt + Metzgerei): eine führt, die zweite bekommt einen eigenen Bereich und eine eigene Seite in ihrer CI.
- Schriften lokal (woff2 aus `assets/baukasten/assets/fonts/` oder Google Fonts herunterladen, nie extern laden), passend zum Logo.
- **Fotos:** Menschen und echte Momente vor Deko. Keine unscharfen Ausschnitte oder Hochskalierungen; lieber ein Foto weniger oder ein Platzhalter. Keine Fotos aus Google Street View oder fremden Quellen. Personen im Bild namentlich mit Rolle nennen, wenn der Laden das möchte. Bekannte Personen nur mit schriftlicher Einwilligung.

## 3. Umsetzung (Clean Architecture)
Ordner `arbeit/kunden/<slug>/`: `inhalt.json` (einzige Quelle), `templates/` (`_layout.html`, `_macros.html`, je Seite eine Datei), `assets/css|js|img|fonts`, `build.py` → `dist/`, `README.md`, `quelle/` (Originale).
- Keine Inhalte doppelt: Zeiten-Kurzform, Fußzeile, JSON-LD und JS lesen aus `inhalt.json`.
- Bilder als WebP in 800/1600 mit `srcset`, `width`/`height`, `loading="lazy"` unter dem ersten Bildschirm, das Hauptbild mit `fetchpriority="high"`.
- Progressive Enhancement: alles funktioniert ohne JS. JS nur für Kleines (z. B. „Jetzt geöffnet“).
- Formular in Schritten nur bei echtem Bedarf (sonst Anrufen, WhatsApp, Route).

## 4. UX und UI (Handy zuerst)
- Erster Bildschirm am Handy: Name, H1 mit Branche und Ort, ein Satz, „Anrufen“ und „Route“, Status „Jetzt geöffnet“.
- Feste Anrufleiste unten am Handy, Sprungmarke „Zum Inhalt“, sichtbarer Fokus, Knöpfe ≥ 44 px.
- Vertrauen: Familie/Team mit Namen, echte Bewertungen mit Quelle und Stand, Zertifikate (z. B. halal) nur belegt.
- Bei 390 px kein waagrechtes Scrollen. Screenshots am Handy (vorher scrollen, damit Lazy-Bilder laden) und am PC ansehen und verbessern.

## 5. SEO
- Pro Seite eigener Title (Branche + Ort · Name) und Description, eine H1, canonical, Open Graph mit `og-bild.jpg` (1200×630).
- JSON-LD: passender Typ (z. B. `GroceryStore`, `ButcherShop` als `department`), `geo` (Nominatim), Zeiten, `sameAs`; auf Unterseiten `BreadcrumbList`.
- `sitemap.xml`, `robots.txt` (bis zum Livegang `Disallow: /` und `noindex`), `404.html`. Interne Links zwischen den Seiten.
- Nach dem Livegang: Google-Profil (Website, Telefon), Instagram-Bio, Search Console.

## 6. Kosten, Vorschau, Livegang
- Domain und Hosting auf den Namen des Ladens vergleichen (Erst- und Verlängerungspreis, E-Mail, AVV) → `kosten-domain-hosting.md`. Nichts bestellen ohne Ja.
- Vorschau-PDF im Handy-Format mit `raster_pdf.py`.
- Vor der Vorschau den **Profi-Check** aus `design-qualitaet.md` (Abschnitt 8) an Screenshots PC und Handy abhaken.
- **Korrekturrunden und spätere Änderungen:** vorher `vergleich.py --sichern dist`, danach `vergleich.py <sicherung> dist`. Vorher/Nachher-Bilder dem Kunden zeigen, Seitenlängen und „kein waagrechtes Scrollen“ mit angeben.
- `website_check.py dist` vor der Vorschau, `--live` vor dem Livegang. Ergebnis zeigen. **Kein Livegang mit ✗.** Offene Punkte ehrlich als Liste.
