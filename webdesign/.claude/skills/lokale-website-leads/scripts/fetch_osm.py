"""Holt unabhängige Läden (keine Ketten) eines Gebiets aus OpenStreetMap.

Aufruf:
    python fetch_osm.py --bbox SÜD,WEST,NORD,OST --out osm.json
    python fetch_osm.py --area-name "68159" --out osm.json    (Grenze per Name, z. B. PLZ-Gebiet; nur Overpass)

Erst werden mehrere Overpass-Server versucht. Sind alle überlastet und eine --bbox ist
angegeben, nutzt das Skript die normale OSM-API (/api/0.6/map). Die reicht für kleine
Gebiete wie eine Altstadt (ca. 1 x 1 km).
Ergebnis: {"elements": [{"type", "id", "tags", "center": {"lat", "lon"}}]}
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

OVERPASS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter",
            "https://overpass.private.coffee/api/interpreter"]
AMENITY = ["restaurant", "cafe", "bar", "pub", "fast_food", "ice_cream", "dentist", "doctors", "veterinary"]
UA = "lokale-website-leads/1.0"


def interessant(t):
    if not t.get("name") or "brand" in t or "brand:wikidata" in t:
        return False
    return "shop" in t or "craft" in t or t.get("amenity") in AMENITY or t.get("leisure") == "fitness_centre"


def overpass(filter_):
    """filter_ ist entweder '(s,w,n,o)' oder '(area.a)' mit vorangestellter Area-Definition."""
    vorab, f = filter_
    q = (f'[out:json][timeout:90];{vorab}(nwr["shop"]{f};nwr["amenity"~"^({"|".join(AMENITY)})$"]{f};'
         f'nwr["craft"]{f};nwr["leisure"="fitness_centre"]{f};);out center tags;')
    for url in OVERPASS:
        try:
            body = urllib.parse.urlencode({"data": q}).encode()
            req = urllib.request.Request(url, body, {"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                txt = r.read().decode("utf-8")
            if txt.lstrip().startswith("{"):
                return [e for e in json.loads(txt)["elements"] if interessant(e.get("tags", {}))]
            print("  Overpass überlastet:", url, file=sys.stderr)
        except Exception as e:
            print("  Overpass-Fehler:", url, type(e).__name__, file=sys.stderr)
        time.sleep(4)
    return None


def osm_api(s, w, n, o):
    url = f"https://api.openstreetmap.org/api/0.6/map?bbox={w},{s},{o},{n}"
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=180) as r:
        root = ET.fromstring(r.read())
    nodes = {x.get("id"): (float(x.get("lat")), float(x.get("lon"))) for x in root.iter("node")}
    out = []
    for el in list(root.iter("node")) + list(root.iter("way")):
        t = {x.get("k"): x.get("v") for x in el.iter("tag")}
        if not interessant(t):
            continue
        if el.tag == "node":
            lat, lon = float(el.get("lat")), float(el.get("lon"))
        else:
            pts = [nodes[nd.get("ref")] for nd in el.iter("nd") if nd.get("ref") in nodes]
            if not pts:
                continue
            lat, lon = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        out.append({"type": el.tag, "id": el.get("id"), "tags": t, "center": {"lat": lat, "lon": lon}})
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bbox", help="süd,west,nord,ost in Grad, z. B. 48.5155,9.048,48.5255,9.064")
    ap.add_argument("--area-name", help='Name einer OSM-Grenze, z. B. "68159"')
    ap.add_argument("--out", default="osm.json")
    a = ap.parse_args()
    if not (a.bbox or a.area_name):
        sys.exit("Bitte --bbox oder --area-name angeben.")
    els = None
    if a.area_name:
        els = overpass((f'area["name"="{a.area_name}"]->.a;', "(area.a)"))
    if els is None and a.bbox:
        s, w, n, o = (float(x) for x in a.bbox.split(","))
        els = overpass(("", f"({s},{w},{n},{o})"))
        if els is None:
            print("  Weiche auf OSM-API aus (nur für kleine Gebiete).", file=sys.stderr)
            els = osm_api(s, w, n, o)
    if els is None:
        sys.exit("Keine Daten bekommen. Mit --bbox erneut versuchen oder später.")
    json.dump({"elements": els}, open(a.out, "w", encoding="utf-8"), ensure_ascii=False)
    mit = sum(1 for e in els if any(k in e["tags"] for k in ("website", "contact:website", "url")))
    print(f"{len(els)} unabhängige Läden, davon {mit} mit Website → {a.out}")
