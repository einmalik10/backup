"""Baut das lokale Lead-Board (eine HTML-Datei) aus audit.json und optional pruefung.json.

Aufruf:
    python build_leadboard.py --audit audit.json --stadt Tübingen --untertitel "Altstadt" --out leadboard.html
    python build_leadboard.py --audit audit.json --pruefung pruefung.json --stadt Tübingen --out leadboard.html

pruefung.json (Ergebnis der Sichtprüfung, siehe SKILL.md Schritt 3) ist eine Liste von Objekten:
    {"name": "Café Beispiel",            # muss dem Namen in audit.json entsprechen
     "status": "open|closed|unknown",     # läuft der Laden noch?
     "website_qualitaet": "gut|mittel|schlecht|tot|keine",
     "eigene_website": "https://…" oder null,
     "ist_kette": false,
     "reasons": "am Screenshot bestätigte Befunde, kurz",
     "pitch": "ein Satz, was die neue Seite ändern würde",
     "conf": "high|medium|low",
     "q": "Straße oder Gasse (für die Laufroute)",     # optional
     "inhaber": "Vor- und Nachname", "inhaber_quelle": "Impressum|Google|OSM|vor Ort",   # optional, nur belegt
     "inhabergefuehrt": true|false|null,  # Inhaber selbst im Laden? (Impressum Einzelperson, keine Filiale)
     "bewertungen": 312, "sterne": 4.6,   # optional, Google-Profil
     "ausschluss": "Grund",               # optional: z. B. "Arztpraxis", "Behörde", "Konflikt mit Kunde"
     "phone": "", "email": "", "insta": ""}               # optional, überschreibt OSM

Top-Lead (Markierung und Filter im Board) = alle Kriterien erfüllt:
  geprüft offen · keine oder schlechte/tote Website · keine Kette/kein Franchise · nicht ausgeschlossen ·
  inhabergeführt (nicht ausdrücklich false) · Branche mit Bedarf (keine Arztpraxis, Behörde, Bank, Apotheke) ·
  aktiv (wenn bekannt: mindestens --min-bewertungen Google-Bewertungen)
Gesundheitsberufe (healthcare:*, Ärzte, Zahnärzte, Therapeuten, Heilpraktiker) fallen immer heraus (Heilmittelwerbegesetz).
--nur-geprueft: nur Läden, die in pruefung.json stehen (empfohlen für die fertige, präzise Liste).
--sperrgebiete datei.json: Läden in diesen Gebieten fallen immer heraus (Gebiet eines anderen Teams).
--bekannt datei.txt: ein Name pro Zeile (schon Kunde, schon Mappe, Konflikt). Diese Läden kommen nicht ins Board.

Regeln:
- Läden mit Website kommen ab --min-score (Standard 30) ins Board.
- Läden OHNE Website kommen nur ins Board, wenn pruefung.json sie als offen bestätigt (oder mit --mit-ohne-website).
- Ketten und geschlossene Läden fallen heraus.
Das Ergebnis enthält Kontaktdaten Dritter und bleibt lokal (nicht ins Git-Repo, siehe .gitignore).
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path

HIER = Path(__file__).resolve().parent
TEMPLATE = HIER.parent / "assets" / "leadboard" / "leadboard.html"

GRUPPEN = {
    "Gastro": {"restaurant", "cafe", "bar", "pub", "fast_food", "ice_cream", "bakery", "confectionery", "butcher", "deli",
               "pastry", "coffee", "tea", "chocolate", "beverages", "wine", "greengrocer", "cheese", "seafood"},
    "Beauty": {"hairdresser", "beauty", "massage", "cosmetics", "tattoo", "nails", "barber", "hairdresser_supply", "perfumery"},
    "Gesundheit": {"dentist", "doctors", "veterinary", "optician", "hearing_aids", "chemist", "medical_supply", "fitness_centre",
                   "herbalist", "health_food", "physiotherapist"},
    "Handel": {"clothes", "shoes", "jewelry", "gift", "books", "furniture", "florist", "toys", "bag", "boutique", "antiques",
               "electronics", "mobile_phone", "computer", "sports", "bicycle", "music", "art", "fabric", "kitchen", "carpet",
               "interior_decoration", "stationery", "second_hand", "variety_store", "photo", "craft"},
}


# Bekannte Ketten und Franchises (Namensanfang, klein). Ergänzen, wenn neue auffallen.
KETTEN = ["mcdonald", "burger king", "subway", "kfc", "domino", "pizza hut", "starbucks", "vapiano", "nordsee", "dean & david",
          "backwerk", "back-factory", "kamps", "le crobag", "ditsch", "yorma", "coffee fellows", "espresso house", "tchibo",
          "dm-drogerie", "dm ", "rossmann", "müller", "douglas", "fressnapf", "deichmann", "fielmann", "apollo", "pearle",
          "klier", "essanelle", "hairkiller", "cut & go", "super cut", "telekom", "vodafone", "o2 ", "1&1", "aldi", "lidl",
          "rewe", "edeka", "netto", "penny", "kaufland", "tegut", "alnatura", "denns", "h&m", "zara", "c&a", "kik", "tedi",
          "action", "nanu-nana", "depot", "thalia", "osiander", "mayersche", "hugendubel", "sparkasse", "volksbank",
          "commerzbank", "deutsche bank", "postbank", "santander", "targobank", "l'osteria", "hans im glück", "block house",
          "peter pane", "losteria", "joey's", "call a pizza", "smileys", "frittenwerk", "burgerme", "five guys", "taco bell",
          "dunkin", "cinnabon", "ben & jerry", "eiscafé venezia", "intersport", "decathlon", "jack wolfskin", "esprit",
          "s.oliver", "tom tailor", "only ", "vero moda", "jack & jones", "snipes", "foot locker", "görtz", "mister spex",
          "mcfit", "fitx", "clever fit", "john reed", "kieser", "mrs. sporty", "body street", "town & country", "remax",
          "engel & völkers", "von poll", "allianz", "ergo", "huk", "devk", "axa", "zurich", "signal iduna", "lvm", "provinzial"]
# Kategorien ohne Bedarf oder mit Werbe-Einschränkungen (Heilmittelwerbegesetz, Behörden, Filialbetriebe)
NIE = {"doctors", "dentist", "hospital", "clinic", "pharmacy", "bank", "atm", "townhall", "government", "police", "post_office",
       "school", "kindergarten", "university", "college", "place_of_worship", "library", "fuel", "car_rental", "bus_station",
       "social_facility", "community_centre", "courthouse", "embassy", "fire_station", "public_bookcase", "toilets", "parking"}


def ist_kette(name):
    n = name.lower().strip()
    return any(n.startswith(k) or f" {k.strip()} " in f" {n} " for k in KETTEN)


def gruppe(cat):
    c = (cat or "").split(":")[-1]
    for g, s in GRUPPEN.items():
        if c in s:
            return g
    return "Sonstiges"


def strasse(addr):
    a = re.sub(r"\s+", " ", (addr or "").strip())
    return re.sub(r"\s+\d+\s*[a-zA-Z]?(\s*[-–/]\s*\d+\s*[a-zA-Z]?)?$", "", a).strip()


def lead_id(name, addr):
    return hashlib.sha1(f"{name}|{addr}".lower().encode("utf-8")).hexdigest()[:10]


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audit", required=True, help="audit.json aus audit.py")
    ap.add_argument("--pruefung", help="pruefung.json mit bestätigten Befunden (optional)")
    ap.add_argument("--stadt", required=True)
    ap.add_argument("--untertitel", default="")
    ap.add_argument("--min-score", type=int, default=30)
    ap.add_argument("--mit-ohne-website", action="store_true", help="auch ungeprüfte Läden ohne OSM-Website aufnehmen (viel Rauschen)")
    ap.add_argument("--bekannt", help="Textdatei: ein Ladenname pro Zeile, der nicht ins Board soll (Kunde, schon Mappe, Konflikt)")
    ap.add_argument("--min-bewertungen", type=int, default=20, help="Top-Lead nur ab so vielen Google-Bewertungen (wenn bekannt)")
    ap.add_argument("--nur-geprueft", action="store_true", help="nur Läden aus pruefung.json ins Board (präzise Liste)")
    ap.add_argument("--sperrgebiete", help="JSON-Liste [{name, bbox:[S,W,N,O]}]: Läden darin kommen nie ins Board (Gebiet eines anderen Teams)")
    ap.add_argument("--out", default="leadboard.html")
    ap.add_argument("--json-out", help="zusätzlich die Lead-Liste als JSON schreiben")
    # Feld "ort" (aus fetch_gebiete.py über audit.json oder aus pruefung.json) → Ort-Filter im Board
    a = ap.parse_args()

    audit = json.load(open(a.audit, encoding="utf-8"))
    pr = {}
    if a.pruefung:
        for p in json.load(open(a.pruefung, encoding="utf-8")):
            pr[p["name"].strip().lower()] = p

    bekannt = set()
    if a.bekannt and Path(a.bekannt).exists():
        bekannt = {z.strip().lower() for z in Path(a.bekannt).read_text(encoding="utf-8").splitlines() if z.strip() and not z.startswith("#")}
    sperr = []
    if a.sperrgebiete and Path(a.sperrgebiete).exists():
        sperr = json.load(open(a.sperrgebiete, encoding="utf-8"))
    leads, raus = [], {"sperrgebiet": 0, "kette": 0, "geschlossen": 0, "score": 0, "ohne_website_ungeprueft": 0, "branche_ausgeschlossen": 0,
                       "bekannt": 0, "ausschluss": 0}
    for r in audit:
        name = r["name"].strip()
        p = pr.get(name.lower(), {})
        hat_site = bool(r.get("website")) and p.get("eigene_website", r.get("website")) is not None
        website = p.get("eigene_website", r.get("website", "")) or ""
        kat = (r.get("cat") or "").split(":")[-1]
        try:
            la, lo = float(r.get("lat")), float(r.get("lon"))
            if any(g["bbox"][0] <= la <= g["bbox"][2] and g["bbox"][1] <= lo <= g["bbox"][3] for g in sperr):
                raus["sperrgebiet"] += 1
                continue
        except (TypeError, ValueError):
            pass
        if name.lower() in bekannt or any(name.lower().startswith(x) for x in bekannt if len(x) > 5):
            raus["bekannt"] += 1
            continue
        if p.get("ausschluss"):
            raus["ausschluss"] += 1
            continue
        if a.nur_geprueft and not p:
            raus["score"] += 1
            continue
        if kat in NIE or (r.get("cat") or "").startswith("healthcare"):
            raus["branche_ausgeschlossen"] += 1
            continue
        if p.get("ist_kette") or (p.get("ist_kette") is None and ist_kette(name)):
            raus["kette"] += 1
            continue
        if p.get("status") == "closed":
            raus["geschlossen"] += 1
            continue
        if not hat_site:
            if not (p.get("status") == "open" or a.mit_ohne_website):
                raus["ohne_website_ungeprueft"] += 1
                continue
            score = int(p.get("score", 60))
        else:
            score = min(100, int(p.get("score", r.get("score", 0))))
            if score < a.min_score and not p:
                raus["score"] += 1
                continue
        addr = (r.get("addr") or "").strip()
        ort = p.get("ort") or r.get("ort", "")
        quali = p.get("website_qualitaet", "")
        bew = p.get("bewertungen")
        top = (p.get("status") == "open" and (not hat_site or quali in ("schlecht", "tot", "keine"))
               and p.get("inhabergefuehrt") is not False and (bew is None or bew >= a.min_bewertungen))
        warum = []
        if top:
            warum.append("keine Website" if not hat_site or quali == "keine" else f"Website {quali}")
            if p.get("inhabergefuehrt"):
                warum.append("inhabergeführt")
            if bew:
                warum.append(f"{bew} Bewertungen" + (f" · {p.get('sterne')} ★" if p.get("sterne") else ""))
        leads.append({
            "inhaber": p.get("inhaber", ""),
            "inhaber_quelle": p.get("inhaber_quelle", ""),
            "ig": p.get("inhabergefuehrt"),
            "bew": bew, "sterne": p.get("sterne"),
            "top": bool(top), "top_warum": " · ".join(warum),
            "id": lead_id(name, addr),
            "list": "bad" if hat_site else "none",
            "name": name,
            "cat": r.get("cat", ""),
            "group": gruppe(r.get("cat", "")),
            "addr": addr,
            "ort": ort,
            "q": p.get("q", strasse(addr)),
            "ok": p.get("status") == "open",
            "website": website,
            "verdict": p.get("website_qualitaet", ""),
            "presence": p.get("presence", ""),
            "reasons": p.get("reasons", ""),
            "auto": r.get("issues", ""),
            "pitch": p.get("pitch", ""),
            "phone": p.get("phone", r.get("phone", "")),
            "email": p.get("email", r.get("email", "")),
            "insta": p.get("insta", ""),
            "maps": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote_plus(f"{name} {addr} {ort or a.stadt}"),
            "conf": p.get("conf", ""),
            "score": score,
        })
    leads.sort(key=lambda l: (not l["top"], -l["score"]))

    tpl = TEMPLATE.read_text(encoding="utf-8")
    daten = json.dumps(leads, ensure_ascii=False).replace("</", "<\\/")
    key = "lb-" + re.sub(r"[^a-z0-9]+", "-", a.stadt.lower()).strip("-")
    html = (tpl.replace("/*__LEADS__*/[]", daten)
               .replace("__TITLE__", f"{a.stadt} Lead-Board")
               .replace("__SUB__", a.untertitel)
               .replace("__KEY__", key)
               .replace("__STAMP__", datetime.date.today().strftime("%d.%m.%Y")))
    Path(a.out).write_text(html, encoding="utf-8")
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(leads, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(1 for l in leads if l["ok"])
    print(f"{len(leads)} Leads im Board ({ok} als offen bestätigt, {sum(l['top'] for l in leads)} Top-Leads) -> {a.out}")
    print("Aussortiert:", ", ".join(f"{k}={v}" for k, v in raus.items()))
    if raus["ohne_website_ungeprueft"]:
        print("Hinweis: Läden ohne Website laut OSM wurden nicht aufgenommen, weil sie erst geprüft werden müssen "
              "(pruefung.json mit status=open) oder mit --mit-ohne-website.", file=sys.stderr)


if __name__ == "__main__":
    main()
