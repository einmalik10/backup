"""Führt Ergebnisse von Subagenten (res*.json) in pruefung.json zusammen.

Aufruf:
    python merge_pruefung.py pruefung.json res1.json res2.json ... [--ueberschreiben]

Zuordnung über den Ladennamen (Groß/Klein egal). Leere Felder in pruefung.json werden gefüllt,
vorhandene Werte bleiben, außer mit --ueberschreiben. Neue Läden aus den Ergebnissen werden angehängt.
Gibt eine kurze Statistik aus (Inhaber gefunden, Ketten erkannt, ohne Beleg).
"""
import json
import sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
ueber = "--ueberschreiben" in sys.argv
if len(args) < 2:
    sys.exit(__doc__)
ziel, quellen = args[0], args[1:]
try:
    pr = json.load(open(ziel, encoding="utf-8"))
except FileNotFoundError:
    pr = []
idx = {p["name"].strip().lower(): p for p in pr}
neu = gefuellt = 0
for q in quellen:
    try:
        daten = json.load(open(q, encoding="utf-8"))
    except Exception as e:
        print(f"! {q}: {e}"); continue
    for r in daten:
        if not isinstance(r, dict) or not r.get("name"):
            continue
        k = r["name"].strip().lower()
        p = idx.get(k)
        if p is None:
            p = {"name": r["name"]}; pr.append(p); idx[k] = p; neu += 1
        for f, v in r.items():
            if f == "name" or v in (None, "", []):
                continue
            if ueber or p.get(f) in (None, "", []):
                p[f] = v; gefuellt += 1
        if r.get("inhaber") and not r.get("inhaber_quelle") and not p.get("inhaber_quelle"):
            p["inhaber_quelle"] = "Recherche"
json.dump(pr, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
mit = sum(1 for p in pr if p.get("inhaber"))
ketten = sum(1 for p in pr if p.get("ist_kette") is True)
print(f"{len(pr)} Läden · {mit} mit Inhaber · {ketten} als Kette erkannt · {gefuellt} Felder gefüllt · {neu} neu -> {ziel}")
