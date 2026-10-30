"""Automatischer Website-Check für alle Läden aus fetch_osm.py.

Aufruf:
    python audit.py osm.json --out audit        → audit.json + audit.csv (Excel-tauglich, ; getrennt)

Bewertet jede Website mit einem Score (höher = schlechter = besserer Lead) und listet
Läden OHNE Website separat (score 100, "keine Website laut OSM").

Wichtig: Das ist nur ein VORFILTER. Jeder Befund muss vor der Verwendung in einer Mappe
am echten Screenshot geprüft werden (siehe SKILL.md, „Verifizieren“).
"""
import argparse
import concurrent.futures as cf
import csv
import json
import re
import time

import requests
import urllib3

urllib3.disable_warnings()
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36",
     "Accept": "text/html,application/xhtml+xml,*/*;q=0.8", "Accept-Language": "de-DE,de;q=0.9"}
UNWICHTIG = {"vacant", "kiosk", "vending_machine", "bookmaker", "tobacco", "e-cigarette", "lottery", "charity",
             "convenience", "supermarket", "money_lender", "pawnbroker", "erotic", "ticket", "newsagent"}
PARKED = re.compile(r"(domain|website)[^<]{0,40}(zu verkaufen|for sale|is parked|geparkt|steht zum verkauf)|sedoparking|parkingcrew|bodis\.com", re.I)


def kategorie(t):
    return t.get("shop") or t.get("amenity") or t.get("craft") or t.get("leisure") or ""


def pruefe(r):
    u = r["website"]
    if not u:
        r.update(score=100, issues="keine Website laut OSM (prüfen!)")
        return r
    u = u if u.startswith("http") else "http://" + u
    iss, s = [], 0
    try:
        t0 = time.time()
        x = requests.get(u, headers=H, timeout=15, verify=False)
        dt = time.time() - t0
        x.encoding = x.apparent_encoding or x.encoding     # sonst falsche "kaputte Umlaute"
        hl = x.text[:400000].lower()
        r["final_url"] = x.url
        if x.status_code >= 400:
            iss.append(f"HTTP {x.status_code}"); s += 50
        if not x.url.startswith("https"):
            try:
                requests.get("https://" + x.url.split("://", 1)[1], headers=H, timeout=8)
                iss.append("http ohne Weiterleitung auf https"); s += 5
            except Exception:
                iss.append("kein HTTPS"); s += 25
        if 'name="viewport"' not in hl and "name='viewport'" not in hl and "name=viewport" not in hl:
            iss.append("nicht mobil-optimiert"); s += 30
        ys = [int(y) for y in re.findall(r"(?:©|&copy;|copyright)\s*(?:\d{4}\s*[-–]\s*)?(20[0-2]\d|19\d\d)", hl)]
        if ys and max(ys) <= time.localtime().tm_year - 4:
            iss.append(f"Copyright {max(ys)}"); s += 10 + min(20, (time.localtime().tm_year - max(ys)) * 3)
        if re.search(r"<frameset|\.swf|<marquee|<font ", hl):
            iss.append("Uralt-HTML/Flash"); s += 30
        if any(k in x.url for k in ("facebook.com", "instagram.com", "business.site", "linktr.ee")):
            iss.append("nur Social/Linkseite"); s += 30
        if PARKED.search(hl):
            iss.append("Domain geparkt/tot"); s += 70
        if len(re.sub(r"<[^>]+>", "", hl)) < 300:
            iss.append("fast kein Inhalt"); s += 20
        if dt > 8:
            iss.append(f"langsam {dt:.0f}s"); s += 10
    except requests.exceptions.SSLError:
        iss.append("SSL-Fehler"); s += 40
    except Exception:
        iss.append("nicht erreichbar (geschlossen? prüfen)"); s += 60
    r.update(score=s, issues="; ".join(iss) or "ok")
    return r


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("osm")
    ap.add_argument("--out", default="audit")
    ap.add_argument("--threads", type=int, default=6, help="niedrig halten, sonst 403/Timeouts durch Bot-Schutz")
    a = ap.parse_args()
    rows = []
    for e in json.load(open(a.osm, encoding="utf-8"))["elements"]:
        t = e["tags"]
        cat = kategorie(t)
        if cat in UNWICHTIG:
            continue
        c = e.get("center", e)
        rows.append(dict(name=t["name"], cat=cat,
                         addr=(t.get("addr:street") or t.get("addr:place") or "") + " " + t.get("addr:housenumber", ""),
                         phone=t.get("phone") or t.get("contact:phone", ""), email=t.get("email") or t.get("contact:email", ""),
                         website=(t.get("website") or t.get("contact:website") or t.get("url") or "").strip(),
                         lat=c.get("lat"), lon=c.get("lon"), ort=e.get("ort", "")))
    with cf.ThreadPoolExecutor(a.threads) as p:
        res = list(p.map(pruefe, rows))
    res.sort(key=lambda r: -r["score"])
    json.dump(res, open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    with open(a.out + ".csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["score", "name", "cat", "addr", "website", "issues", "phone", "email"], delimiter=";", extrasaction="ignore")
        w.writeheader(); w.writerows(res)
    mit = [r for r in res if r["website"]]
    print(f"{len(res)} Läden geprüft · {len(mit)} mit Website · {len(res) - len(mit)} ohne")
    for r in mit[:30]:
        print(f"{r['score']:>4} | {r['name'][:32]:<32} | {r['cat'][:14]:<14} | {r['addr'][:22]:<22} | {r['issues']}")
