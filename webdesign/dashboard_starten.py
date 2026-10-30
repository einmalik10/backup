"""Startet das Lead-Dashboard: sucht das neueste arbeit/**/leadboard.html, startet den Server und öffnet den Browser.

Aufruf: Doppelklick auf dashboard-starten.bat (oder: python dashboard_starten.py)
Nimmt den ersten freien Port ab 8770. Fenster schließen = Server aus.
"""
import functools
import http.server
import socket
import sys
import webbrowser
from pathlib import Path

PORTS = range(8770, 8800)
ARBEIT = Path(__file__).resolve().parent / "arbeit"


class Leise(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class Server(http.server.ThreadingHTTPServer):
    allow_reuse_address = False  # sonst teilen sich unter Windows zwei Server denselben Port


def frei(port):
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


boards = sorted(ARBEIT.rglob("leadboard.html"), key=lambda p: p.stat().st_mtime, reverse=True)
if not boards:
    sys.exit("Kein leadboard.html in arbeit/ gefunden. Erst in Claude Code /dashboard <Ort> ausführen.")
board = boards[0]
handler = functools.partial(Leise, directory=str(board.parent))

for port in PORTS:
    if not frei(port):
        continue
    try:
        srv = Server(("127.0.0.1", port), handler)
    except OSError:
        continue
    break
else:
    sys.exit(f"Kein freier Port zwischen {PORTS.start} und {PORTS.stop - 1}.")

url = f"http://localhost:{port}/leadboard.html"
print(f"Dashboard: {board.parent.name}")
print(f"Adresse:   {url}")
print("Zum Beenden dieses Fenster schließen.")
with srv:
    webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
