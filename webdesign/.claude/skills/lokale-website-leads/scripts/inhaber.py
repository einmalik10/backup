"""Liest Inhaber bzw. Geschäftsführer aus dem Impressum vieler Websites (parallel, ohne Browser).

Aufruf:
    python inhaber.py --pruefung pruefung.json [--out inhaber.json]     # nimmt eigene_website aus der Prüfdatei
    python inhaber.py https://laden1.de https://laden2.de               # einzelne Seiten

Ergebnis (inhaber.json): {"Ladenname": {"inhaber": "...", "rolle": "Inhaber|Geschäftsführer|Vertreten durch",
                         "rechtsform": "GmbH|UG|e.K.|GbR|...", "impressum_url": "...", "hinweis": "..."}}
Mit --einfuegen werden inhaber, inhaber_quelle="Impressum" und inhabergefuehrt direkt in pruefung.json geschrieben
(nur wo noch kein Inhaber steht). Treffer sind Vorschläge: bei Top-Leads Stichproben am Impressum prüfen.
"""
import argparse
import concurrent.futures as cf
import html
import json
import re
import sys
from urllib.parse import urljoin

import requests
import urllib3

urllib3.disable_warnings()
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0) Chrome/129 Safari/537.36", "Accept-Language": "de-DE"}
SCHLUESSEL = [("Inhaber", re.compile(r"Inhaber(?:in)?", re.I)), ("Geschäftsführer", re.compile(r"Geschäftsführ(?:er|erin|ung|ende)", re.I)),
              ("Vertreten durch", re.compile(r"vertreten\s+durch|vertretungsberechtigt", re.I)), ("Betreiber", re.compile(r"Betreiber(?:in)?", re.I)),
              ("Verantwortlich", re.compile(r"verantwortlich\s+(?:für den Inhalt|i\.\s?S\.|im Sinne|nach)", re.I)),
              ("Angaben § 5", re.compile(r"Angaben\s+gem(?:ä|ae)ß\s+§\s*5|§\s*5\s*(?:TMG|DDG)", re.I))]
WORT = r"[A-ZÄÖÜ][a-zäöüßéèáàíóúçñş\-']+"
PERSON = re.compile(r"^(?:(?:Herr|Frau|Dr\.|Dipl\.-[A-Za-z]+\.?|Prof\.)\s+)*(" + WORT + r"(?:[ 	]+(?:von|van|de|del|da|di|el|al|zu)?[ 	]*" + WORT + r"){1,3})\s*[,;]?$")
NICHT = re.compile(r"Muster|Impressum|Datenschutz|Telefon|Telefax|Straße|Strasse|Platz|Weg|Allee|Kontakt|Angaben|Verantwortlich|Register|Amtsgericht|Haftung|Umsatzsteuer|Steuer|Mannheim|Tübingen|Deutschland|Germany|Restaurant|Salon|Praxis|Studio|Café|Cafe|Bar|Bistro|Friseur|Kosmetik|Inhaber|Geschäft|Gesellschaft|Vertret|Haus|Hotel|Team|Online|Website|Webseite|Agentur|Design|Kanzlei|Zentrum|Institut|Service|Handel|Group|Gruppe|Holding|Partner|Beratung|Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag", re.I)
FORMEN = [("GmbH & Co. KG", r"GmbH\s*&\s*Co\.?\s*KG"), ("GmbH", r"\bGmbH\b"), ("UG", r"\bUG\b"), ("e.K.", r"\be\.\s?K\.?"),
          ("GbR", r"\bGbR\b"), ("AG", r"\bAG\b"), ("KG", r"\bKG\b"), ("OHG", r"\bOHG\b")]
KETTE = re.compile(r"Franchise|Lizenznehmer|Systempartner|Filiale der|Zentrale", re.I)


def text(s):
    s = re.sub(r"(?s)<(script|style|noscript).*?</\1>", " ", s)
    s = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</h\d>", "\n", s, flags=re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def holen(u):
    r = requests.get(u, headers=H, timeout=12, verify=False)
    r.encoding = r.apparent_encoding or r.encoding
    return r


def finde(url):
    if not url:
        return {"hinweis": "keine Website"}
    if not re.match(r"https?://", url):
        url = "http://" + url
    try:
        r = holen(url)
    except Exception as e:
        return {"hinweis": f"nicht erreichbar ({type(e).__name__})"}
    kandidaten = [urljoin(r.url, l) for l in re.findall(r'href=["\']([^"\'#]+)', r.text) if re.search(r"impress|imprint|kontakt", l, re.I)]
    kandidaten += [urljoin(r.url, p) for p in ("/impressum", "/impressum.html", "/impressum/", "/imprint")]
    gesehen, seiten = set(), [(r.url, r.text)]
    for k in kandidaten[:6]:
        if k in gesehen:
            continue
        gesehen.add(k)
        try:
            rr = holen(k)
            if rr.ok and "impress" in rr.text.lower():
                seiten.insert(0, (rr.url, rr.text))
                break
        except Exception:
            pass
    for u, h in seiten:
        t = text(h)
        zeilen = [re.sub(r"[ 	 ]+", " ", z).strip(" :-–	") for z in t.splitlines()]
        zeilen = [z for z in zeilen if z]
        form = next((f for f, rx in FORMEN if re.search(rx, t)), "")
        for rolle, rx in SCHLUESSEL:
            for i, z in enumerate(zeilen):
                m = rx.search(z)
                if not m:
                    continue
                rest = z[m.end():].strip(" :-–.")
                rest = re.sub(r"^(?:den|die|der)\s+(?:Geschäftsführer(?:in)?|Inhaber(?:in)?)\s*[:\-–]?\s*", "", rest)
                for kand in [rest] + zeilen[i + 1:i + 4]:
                    kand = re.split(r"\s{2,}|\||,\s*(?=\d)|\s+(?:Tel|Telefon|Fax|E-Mail|Mail|Str\.)", kand)[0].strip()
                    pm = PERSON.match(kand)
                    if pm and not NICHT.search(pm.group(1)):
                        return {"inhaber": pm.group(1), "rolle": rolle if rolle not in ("Angaben § 5", "Verantwortlich") else "laut Impressum",
                                "rechtsform": form, "impressum_url": u, "hinweis": "Franchise-Hinweis im Impressum" if KETTE.search(t) else ""}
    return {"hinweis": "kein Name im Impressum gefunden", "impressum_url": seiten[0][0]}


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--pruefung")
    ap.add_argument("--out", default="inhaber.json")
    ap.add_argument("--einfuegen", action="store_true", help="Treffer in pruefung.json eintragen")
    a = ap.parse_args()
    jobs = {}
    if a.pruefung:
        pr = json.load(open(a.pruefung, encoding="utf-8"))
        for p in pr:
            if p.get("eigene_website") and not p.get("inhaber"):
                jobs[p["name"]] = p["eigene_website"]
    for u in a.urls:
        jobs[u] = u
    erg = {}
    with cf.ThreadPoolExecutor(12) as ex:
        for name, res in zip(jobs, ex.map(finde, jobs.values())):
            erg[name] = res
            print(f"{'✓' if res.get('inhaber') else '·'} {name}: {res.get('inhaber') or res.get('hinweis')}"
                  + (f" ({res['rolle']}, {res['rechtsform']})" if res.get("inhaber") else ""))
    json.dump(erg, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    gefunden = sum(1 for r in erg.values() if r.get("inhaber"))
    print(f"\n{gefunden} von {len(erg)} Inhabern gefunden -> {a.out}")
    if a.pruefung and a.einfuegen:
        for p in pr:
            r = erg.get(p["name"], {})
            if r.get("inhaber") and not p.get("inhaber"):
                p["inhaber"] = r["inhaber"]
                p["inhaber_quelle"] = "Impressum"
                if p.get("inhabergefuehrt") is None:
                    groß = r.get("rechtsform") in ("AG", "GmbH & Co. KG") or r.get("hinweis")
                    p["inhabergefuehrt"] = None if groß else True
                if r.get("hinweis"):
                    p["ist_kette"] = True
        json.dump(pr, open(a.pruefung, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("pruefung.json ergänzt.")


if __name__ == "__main__":
    main()
