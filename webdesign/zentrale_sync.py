"""Spiegelt Maliks Arbeit in den privaten Sammelordner C:\\Users\\Malik\\zentrale und pusht ihn zu GitHub.

Aufruf: python zentrale_sync.py            (kopieren + committen + pushen)
        python zentrale_sync.py --nur-kopieren

Was rein kommt: webdesign (inkl. arbeit/ mit Kunden), second-brain (Obsidian), eigene Skills aus ~/.claude/skills.
Was NIE rein kommt: .env-Dateien, Schlüssel, node_modules, dist, Caches, verschachtelte .git-Ordner,
Screenshots der Lead-Scans (fremde Websites, jederzeit neu erzeugbar), Dateien über 90 MB.
"""
import argparse
import fnmatch
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
ZIEL = HOME / "zentrale"
QUELLEN = {
    "webdesign": HOME / "webdesign",
    "second-brain": HOME / "second-brain",
    "skills": HOME / ".claude" / "skills",
}
NIE_ORDNER = {"node_modules", "dist", "__pycache__", ".git", ".obsidian-cache", "synced"}
NIE_DATEIEN = [".env", ".env.*", "*.env", "*.key", "*.pem", "*.p12", "*.tmp", "Thumbs.db", ".DS_Store",
               "workspace.json", "workspace-mobile.json"]
ERLAUBT_TROTZDEM = [".env.beispiel", ".env.example"]
LEAD_ORDNER = {"boeblingen-sindelfingen", "grossraum", "singen-sigmaringen", "rottenburg"}
BILDER = ["*.png", "*.jpg", "*.jpeg", "*.webp"]
MAX = 90 * 1024 * 1024


def ausschliessen(rel: Path, ist_ordner: bool) -> bool:
    teile = rel.parts
    if any(t in NIE_ORDNER for t in teile):
        return True
    if ist_ordner:
        return False
    name = rel.name
    if any(fnmatch.fnmatch(name, m) for m in ERLAUBT_TROTZDEM):
        return False
    if any(fnmatch.fnmatch(name, m) for m in NIE_DATEIEN):
        return True
    # Screenshots der Lead-Scans: webdesign/arbeit/<lead-ordner>/...
    if len(teile) > 3 and teile[0] == "webdesign" and teile[1] == "arbeit" and teile[2] in LEAD_ORDNER \
            and any(fnmatch.fnmatch(name.lower(), m) for m in BILDER):
        return True
    return False


def spiegeln():
    soll = set()
    for wurzel, quelle in QUELLEN.items():
        for p in quelle.rglob("*"):
            rel = Path(wurzel) / p.relative_to(quelle)
            if ausschliessen(rel, p.is_dir()) or p.is_dir() or p.is_symlink():
                continue
            if p.stat().st_size > MAX:
                print(f"  zu groß, übersprungen: {rel}")
                continue
            soll.add(rel)
            z = ZIEL / rel
            if not z.exists() or z.stat().st_size != p.stat().st_size or z.stat().st_mtime < p.stat().st_mtime - 1:
                z.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, z)
    # Gelöschtes auch im Spiegel löschen (nur in den drei Bereichen)
    for wurzel in QUELLEN:
        for z in sorted((ZIEL / wurzel).rglob("*"), reverse=True) if (ZIEL / wurzel).exists() else []:
            rel = z.relative_to(ZIEL)
            if z.is_file() and rel not in soll:
                z.unlink()
            elif z.is_dir() and not any(z.iterdir()):
                z.rmdir()
    return len(soll)


def git(*args):
    return subprocess.run(["git", "-C", str(ZIEL), *args], capture_output=True, text=True, encoding="utf-8")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--nur-kopieren", action="store_true")
    a = ap.parse_args()
    ZIEL.mkdir(exist_ok=True)
    n = spiegeln()
    print(f"✓ {n} Dateien im Spiegel {ZIEL}")
    if a.nur_kopieren:
        return
    git("add", "-A")
    r = git("commit", "-q", "-m", f"Stand {datetime.now():%Y-%m-%d %H:%M}")
    if "nothing to commit" in (r.stdout + r.stderr):
        print("Keine Änderungen.")
    p = git("push", "-q", "origin", "HEAD")
    print("✓ gepusht" if p.returncode == 0 else "✗ Push fehlgeschlagen:\n" + p.stderr)


if __name__ == "__main__":
    main()
