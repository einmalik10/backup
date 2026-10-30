"""Holt die Läden mehrerer Orte auf einmal aus OpenStreetMap, z. B. das ganze Gebiet aus gebiete.json.

Aufruf (Repo-Wurzel als Bezug):
    python fetch_gebiete.py --gebiete ../../../../gebiete.json --sperrgebiete ../../../../sperrgebiete.json --out osm.json
    python fetch_gebiete.py --gebiete … --orte "Mössingen,Nehren" --out osm.json          (nur einzelne Orte)
    python fetch_gebiete.py --gebiete … --landkreise "Landkreis Sigmaringen,Landkreis Konstanz" --out osm.json

- Gemeinden: Suche der Gemeindegrenze (OSM-Relation, admin_level 8) per Name, Abfrage per Grenze.
  Liefert Overpass für eine Grenze nichts (Fläche fehlt), wird die Box der Grenze genommen und nach addr:city gefiltert.
- Tübinger Teilorte: kleine Boxen (TEILORTE unten), die die Kernstadt nicht berühren.
- Orte unter "nach_absprache" werden übersprungen. Läden in sperrgebiete.json werden nie gespeichert.
Ergebnis wie fetch_osm.py, zusätzlich Feld "ort" pro Laden (audit.py und build_leadboard.py reichen es durch → Ort-Filter im Board).
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from fetch_osm import AMENITY, OVERPASS, UA, interessant, osm_api

# süd, west, nord, ost. Kleine Boxen um die Tübinger Teilorte (außerhalb der Kernstadt), damit sie im Board als eigener Ort erscheinen.
TEILORTE = {
    "Tübingen-Unterjesingen": (48.512, 8.945, 48.528, 8.975),
    "Tübingen-Hirschau": (48.494, 8.980, 48.510, 9.010),
    "Tübingen-Bühl": (48.480, 8.972, 48.494, 9.000),
    "Tübingen-Kilchberg": (48.480, 9.000, 48.4945, 9.025),
    "Tübingen-Weilheim": (48.488, 9.022, 48.4945, 9.048),
    "Tübingen-Hagelloch": (48.527, 8.982, 48.541, 9.012),
    "Tübingen-Pfrondorf": (48.541, 9.085, 48.556, 9.115),
    "Tübingen-Bebenhausen": (48.553, 9.048, 48.568, 9.072),
}
SUCHBOX = "(48.2,8.5,48.8,9.4)"  # Region Tübingen, damit gleichnamige Orte anderswo nicht treffen


def anfrage(q, versuche=3):
    for runde in range(versuche):
        for url in OVERPASS:
            try:
                body = urllib.parse.urlencode({"data": q}).encode()
                req = urllib.request.Request(url, body, {"User-Agent": UA, "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=200) as r:
                    txt = r.read().decode("utf-8")
                if txt.lstrip().startswith("{"):
                    return json.loads(txt)["elements"]
            except Exception as e:
                print("   ", url.split("/")[2], type(e).__name__, getattr(e, "code", ""), file=sys.stderr)
            time.sleep(5)
        time.sleep(20)
    return None


def laeden(vorab, f):
    q = (f'[out:json][timeout:180];{vorab}(nwr["shop"]{f};nwr["amenity"~"^({"|".join(AMENITY)})$"]{f};'
         f'nwr["craft"]{f};nwr["leisure"="fitness_centre"]{f};);out center tags;')
    els = anfrage(q)
    return None if els is None else [e for e in els if interessant(e.get("tags", {}))]


def grenz_ringe(rel_id):
    """Außenringe einer Gemeindegrenze über die OSM-API (für den Box-Notfall, damit Nachbarorte rausfallen)."""
    url = f"https://api.openstreetmap.org/api/0.6/relation/{rel_id}/full"
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=180) as r:
        root = ET.fromstring(r.read())
    nodes = {n.get("id"): (float(n.get("lat")), float(n.get("lon"))) for n in root.iter("node")}
    ways = {w.get("id"): [nodes[nd.get("ref")] for nd in w.iter("nd")] for w in root.iter("way")}
    rel = next(r for r in root.iter("relation") if r.get("id") == str(rel_id))
    segs = [ways[m.get("ref")] for m in rel.iter("member") if m.get("type") == "way" and m.get("role") == "outer"]
    ringe = []
    while segs:
        ring = list(segs.pop(0)); weiter = True
        while weiter and ring[0] != ring[-1]:
            weiter = False
            for i, sg in enumerate(segs):
                if sg[0] == ring[-1]:
                    ring += sg[1:]; segs.pop(i); weiter = True; break
                if sg[-1] == ring[-1]:
                    ring += sg[::-1][1:]; segs.pop(i); weiter = True; break
        ringe.append(ring)
    return ringe


def im_gebiet(la, lo, ringe):
    drin = False
    for ring in ringe:
        for (y1, x1), (y2, x2) in zip(ring, ring[1:]):
            if (y1 > la) != (y2 > la) and lo < (x2 - x1) * (la - y1) / (y2 - y1) + x1:
                drin = not drin
    return drin


def gesperrt(e, sperr):
    c = e.get("center") or {"lat": e.get("lat"), "lon": e.get("lon")}
    la, lo = c.get("lat"), c.get("lon")
    return la is not None and any(g["bbox"][0] <= la <= g["bbox"][2] and g["bbox"][1] <= lo <= g["bbox"][3] for g in sperr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gebiete", required=True)
    ap.add_argument("--sperrgebiete")
    ap.add_argument("--orte", help="Komma-Liste; ohne Angabe alle Orte aus gebiete.json")
    ap.add_argument("--landkreise", help='Komma-Liste ganzer Landkreise, z. B. "Landkreis Sigmaringen,Landkreis Konstanz": alle Gemeinden darin')
    ap.add_argument("--out", default="osm.json")
    a = ap.parse_args()
    geb = json.load(open(a.gebiete, encoding="utf-8"))
    sperr = json.load(open(a.sperrgebiete, encoding="utf-8")) if a.sperrgebiete else []
    gemeinden = [o["name"] for o in geb["orte"] if not o["name"].startswith("Tübinger Teilorte")]
    teilorte = any(o["name"].startswith("Tübinger Teilorte") or o["name"] == "Tübingen" for o in geb["orte"])
    if a.orte:
        wahl = [x.strip() for x in a.orte.split(",")]
        if any(x in geb.get("nach_absprache", []) for x in wahl):
            sys.exit("Orte unter nach_absprache nur nach Freigabe durch den Repo-Inhaber.")
        gemeinden = [g for g in gemeinden if g in wahl]
        teilorte = teilorte and any(x.startswith("Tübingen") for x in wahl)

    if a.landkreise:
        # Alle Gemeinden (admin_level 8) innerhalb der genannten Landkreise; die Liste aus gebiete.json gilt dann nicht
        rels = []
        for lk in [x.strip() for x in a.landkreise.split(",")]:
            q = (f'[out:json][timeout:120];rel["boundary"="administrative"]["admin_level"="6"]["name"="{lk}"];map_to_area->.k;'
                 f'rel(area.k)["boundary"="administrative"]["admin_level"="8"];out ids tags bb;')
            gef = anfrage(q) or []
            print(f"{lk}: {len(gef)} Gemeinden", flush=True)
            rels += gef
        gemeinden = sorted({r["tags"]["name"] for r in rels})
        teilorte = False
    else:
        rx = "|".join(gemeinden)
        rels = anfrage(f'[out:json][timeout:60];rel["boundary"="administrative"]["admin_level"="8"]["name"~"^({rx})$"]{SUCHBOX};out ids tags bb;') or []
    grenzen = {r["tags"]["name"]: r for r in rels}

    out, gesehen = [], set()

    # Bei Box-Abfragen: Läden mit fremder addr:city verwerfen (Nachbarorte, Kernstadt, Orte nach Absprache)
    fremd = {"Tübingen", "Pliezhausen", "Wannweil", "Walddorfhäslach", "Gäufelden", "Hechingen", "Rangendingen", "Nagold",
             *geb.get("nach_absprache", []), *gemeinden}

    def aufnehmen(els, ort, box=False):
        n = 0
        for e in els:
            k = (e["type"], str(e["id"]))
            if k in gesehen or gesperrt(e, sperr):
                continue
            city = e["tags"].get("addr:city", "")
            if box and city in fremd - {ort}:
                continue
            gesehen.add(k); e["ort"] = ort
            e.setdefault("center", {"lat": e.get("lat"), "lon": e.get("lon")})
            out.append(e); n += 1
        return n

    # Teilorte zuerst, damit sie ihren Namen behalten, wenn die ganze Stadt (z. B. Tübingen) danach kommt
    if teilorte:
        for name, (s, w, n_, o) in TEILORTE.items():
            els = laeden("", f"({s},{w},{n_},{o})")
            if els is None:
                els = osm_api(s, w, n_, o)
            print(f"{name}: {aufnehmen(els, name)}", flush=True)
            time.sleep(3)
    for name in gemeinden:
        r = grenzen.get(name)
        if not r:
            print(f"{name}: keine Gemeindegrenze gefunden, übersprungen"); continue
        els = laeden(f"area({3600000000 + r['id']})->.a;", "(area.a)")
        if not els and r.get("bounds"):
            b = r["bounds"]
            els = laeden("", f"({b['minlat']},{b['minlon']},{b['maxlat']},{b['maxlon']})") or []
            try:  # Box enthält Nachbarorte: auf die echte Gemeindegrenze zuschneiden
                ringe = grenz_ringe(r["id"])
                els = [e for e in els if im_gebiet((e.get("center") or e)["lat"], (e.get("center") or e)["lon"], ringe)]
            except Exception as ex:
                print(f"   Grenze für {name} nicht geladen ({type(ex).__name__}), filtere nur nach addr:city", file=sys.stderr)
            n = aufnehmen(els, name, box=True)
        else:
            n = aufnehmen(els or [], name)
        print(f"{name}: {n}", flush=True)
        time.sleep(3)
    Path(a.out).write_text(json.dumps({"elements": out}, ensure_ascii=False), encoding="utf-8")
    mit = sum(1 for e in out if e["tags"].get("website") or e["tags"].get("contact:website"))
    print(f"{len(out)} unabhängige Läden, davon {mit} mit Website → {a.out}")
