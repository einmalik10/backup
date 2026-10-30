# Schema für eine Kundendatei. Kopieren, anpassen, an shots.py und build_mappen.py übergeben.
# Jede Aussage hier landet beim Kunden auf Papier. Nur Geprüftes eintragen, Unbekanntes als [Platzhalter].

ABSENDER = {"name": "DEIN NAME", "telefon": "DEINE NUMMER", "zusatz": "auch per WhatsApp"}

# Gemeinsame Felder für ein Gebiet 
GEBIET = dict(
    stadt="Musterstadt",                      # Kopfzeile der Mappe
    gebiet="in der Musterstädter Altstadt",     # „Für die ersten Kunden …“
    fusszeile="Webdesign für die Region",  # Fußzeile neben dem Namen
    kaffee_text="Ich zeige Ihnen den Entwurf gern persönlich, in 15 Minuten bei Ihnen vor Ort.",
)

KUNDEN = [
  # ── Laden MIT schlechter Website ─────────────────────────────────────────
  dict(GEBIET,
    slug="alte-bruecke",                 # Dateiname der Demo: <demo-base>/<slug>.html
    name="Gasthaus Alte Brücke",
    quadrat="Altstadt",                    # Etikett oben auf Seite 1/2 (Viertel oder Straße)
    branche="Steakhäusle, schwäbische Küche",
    adresse="Brückenstraße 1 · 12345 Musterstadt",
    inhaber="Familie Muster (aus dem Impressum)", # aus dem Impressum; nur für Laufzettel, nicht in der Mappe
    vorher_art="website",
    vorher_url="http://www.alte-bruecke.de/",   # exakt so, wie Kunden sie aufrufen (http → „Nicht sicher“)
    domain="alte-bruecke.de",            # nur echte Domain des Kunden, sonst weglassen
    probleme=[                             # 3 Sätze, jeder am Screenshot belegt. Satz 1 = Untertitel auf Seite 1
      "Die Seite „Speisen“ ist leer: Wer Ihre Karte sucht, findet nichts.",
      "Design aus den frühen 2000ern, nicht fürs Handy, kein HTTPS.",
      "Ihre Geschichte (Haus von 1602, Terrasse am Mühlbach) steht versteckt unter „über uns“."],
    kritik=[                               # rote Pins auf dem PC-Screenshot: (x %, y %, kurzer Text). x > 58 → Text links
      (13, 36, "Seite „Speisen“ ist leer"),
      (78, 50, "Leere gelbe Fläche, nicht fürs Handy"),
      (36, 85, "Keine Reservierung, keine Karte")],
    check=[("Speisekarte online", False), ("Handy-optimiert", False), ("HTTPS / sicher", False),
           ("Reservieren", False), ("Öffnungszeiten online", True)],   # ehrlich, auch ✓ zeigen
    konzept_titel="Der Name ist Kulturgut.",
    konzept="„Alte Brücke“ kennt in Musterstadt jeder. Deshalb steht der Name riesig ganz oben, in Frakturschrift wie Ihr grüner Schriftzug an der Fassade. …",
    farben=[("#1f3d2b", "Tannengrün", "wie Ihr Schriftzug"), ("#c8372d", "Geranienrot", "Knöpfe"),
            ("#4f7f8a", "Mühlbach", "Terrasse"), ("#faf6ec", "Papier", "Hintergrund")],     # genau 4
    schriften=[("UnifrakturMaguntia", "Fraktur wie an der Fassade, nur für den Namen"),
               ("Alegreya", "Kräftige Buchschrift für alle Texte")],                          # Google-Fonts-Namen
    entscheidungen=[                       # 4–5 Begründungen, die ersten 3 erscheinen auf Seite 2
      ("Der Name ganz groß", "„Alte Brücke“ in Fraktur, so wie man das Gasthaus von der Fassade kennt."),
      ("Die Karte endlich online", "Steaks und schwäbische Klassiker, gut lesbar auf dem Handy."),
      ("1602, 45 Plätze, Terrasse", "Drei Zahlen, die sofort zeigen, warum man zu Ihnen kommt."),
      ("Ein Knopf zum Reservieren", "Auf dem Handy ruft er direkt bei Ihnen an.")],
    paket="Standard", preis="890 €", extras="Speisekarte als eigene Seite",
    brauchen=["Ihre Speisekarte mit Preisen", "Fotos von Steaks, Gastraum und Terrasse",
              "Zugang zur Domain alte-bruecke.de", "Wünsche zur Reservierung"],               # genau 4
  ),

  # ── Laden OHNE eigene Website ────────────────────────────────────────────
  dict(
    slug="cafe-beispiel", name="Café Beispiel", quadrat="Markt", branche="Kaffeehaus",
    adresse="Marktplatz 3 · 12345 Musterstadt",
    vorher_art="suche",                    # → nachgestellte, neutral gestaltete Suchansicht (assets/vorher.html)
    suche={"q": "café beispiel mannheim", "name": "Café Beispiel", "typ": "Café in Musterstadt",
           "adresse": "Marktplatz 3, 12345 Musterstadt", "preise": "nur über Fremdportale",
           "treffer": [   # nur Portale, die bei der Recherche wirklich gefunden wurden
             {"kurz": "W", "seite": "Wanderlog", "url": "wanderlog.com › place › cafe-beispiel",
              "titel": "Café Beispiel – Musterstadt", "text": "Reiseportal mit Kurzbeschreibung und Fotos anderer Besucher."},
             {"kurz": "S", "seite": "speisekarte.menu", "url": "speisekarte.menu › restaurants › mannheim",
              "titel": "Café Beispiel – Musterstadt · Speisekarte", "text": "Fremdportal, Angaben ohne Gewähr."},
             {"kurz": "Ö", "seite": "Das Örtliche", "url": "dasoertliche.de › cafes › mannheim",
              "titel": "Cafés in Musterstadt", "text": "Branchenverzeichnis, einer von vielen Einträgen."}]},
    probleme=["Keine eigene Website: Wer sucht, landet auf Fremdportalen mit ungeprüften Angaben.",
              "Das Kulturprogramm (Lesungen, Musik, Ausstellungen) ist online kaum auffindbar.",
              "Die besondere Geschichte des Hauses wird nirgends erzählt."],
    kritik=[(68, 26, "Keine eigene Website"), (24, 19, "Erster Treffer: ein Fremdportal"),
            (24, 45, "Ihre Konkurrenz auf derselben Liste")],   # feste Positionen für die Suchansicht
    check=[("Eigene Website", False), ("Karte online", False), ("Programm online", False),
           ("Öffnungszeiten aus erster Hand", False), ("Bei Google Maps gelistet", True)],
    konzept_titel="Das Schild wird zur Marke.",
    konzept="Das rote Hängeschild an der Fassade kennt jeder, der schon einmal vorbeigegangen ist. …",
    farben=[("#a3161f", "Schildrot", "Marke"), ("#1d1715", "Kaffeeschwarz", "Text"),
            ("#f6f2ec", "Papier", "Hintergrund"), ("#b8955a", "Messing", "Details")],
    schriften=[("Alfa Slab One", "Wie die Buchstaben auf dem Schild"), ("Libre Caslon Text", "Klassische Buchschrift")],
    entscheidungen=[("Kein Coffee to go", "Ihre Haltung wird zur Botschaft."),
                    ("Programm als eigener Bereich", "Termine schicken Sie mir, sie sind am selben Tag online."),
                    ("Laufband mit Stichworten", "In einer Sekunde ist klar, was das Café ausmacht.")],
    paket="Standard", preis="890 €", extras="Neue Programmtermine pflege ich für Sie ein",
    brauchen=["8 bis 12 Fotos", "Aktuelle Karte mit Preisen", "Die nächsten 3 Termine", "Ein Satz zum Gastgeber"],
  ),
]
