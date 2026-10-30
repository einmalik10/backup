"""Liest den Text einer Website und ihrer Impressum-/Kontakt-/Speisekarte-Seiten.

Aufruf:
    python peek.py https://laden1.de http://laden2.de ...

Zeigt pro Seite: Anfang des Textes, wichtige Unterseiten-Links und den Ausschnitt
um „Inhaber“ bzw. „Impressum“. Damit findest du Inhabernamen, Telefon, geschäftliche
E-Mail, Öffnungszeiten, echte Preise und Geschichte für die Demo.
Achtung: Text kann falsch dekodiert sein. Umlaut-Fehler NIE aus diesem Output ableiten,
nur aus einem echten Browser-Screenshot.
"""
import html
import re
import sys

import requests
import urllib3

urllib3.disable_warnings()
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0) Chrome/129 Safari/537.36", "Accept-Language": "de-DE"}
WICHTIG = re.compile(r"impress|kontakt|about|ueber|über|speise|karte|menu|preis|leistung|angebot|team", re.I)


def text(s):
    s = re.sub(r"(?s)<(script|style).*?</\1>", "", s)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def holen(u):
    r = requests.get(u, headers=H, timeout=15, verify=False)
    r.encoding = r.apparent_encoding or r.encoding
    return r


for u in sys.argv[1:]:
    try:
        r = holen(u)
        print("=" * 8, u, r.status_code, r.url)
        print(text(r.text)[:900])
        links = sorted(set(l for l in re.findall(r'href=["\']([^"\'#]+)', r.text) if WICHTIG.search(l)))
        print("UNTERSEITEN:", links[:15])
        for l in [l for l in links if re.search("impress|kontakt", l, re.I)][:2]:
            v = requests.compat.urljoin(r.url, l)
            t = text(holen(v).text)
            i = max(t.lower().find("inhaber"), t.lower().find("impressum"), 0)
            print("  →", v, ":", t[i:i + 500])
    except Exception as e:
        print("=" * 8, u, "FEHLER", type(e).__name__, "(nicht erreichbar ist selbst ein Befund)")
