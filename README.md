# Malik · Zentrale (privat)

Alles an einem Ort: Webdesign (inkl. Kunden), Second Brain (Obsidian), eigene Claude-Skills.
**Privates Repo. Enthält Kundendaten. Nie öffentlich stellen.**

- `webdesign/` – Repo mit Skills, Vorlagen und `arbeit/` (Kunden, Mappen, Demos)
- `second-brain/` – Obsidian-Tresor (in Obsidian als Tresor öffnen)
- `skills/` – eigene Claude-Skills (auf einem neuen Gerät nach `~/.claude/skills/` kopieren)

Nicht enthalten: `.env`/Schlüssel, `node_modules` (mit `npm install` neu holen), Screenshots der Lead-Scans.
Aktualisiert wird vom Windows-PC mit `python webdesign/zentrale_sync.py` (Spiegel, Richtung PC → GitHub).

## Auf dem MacBook
```
git clone https://github.com/einmalik10/backup.git ~/zentrale
cp -R ~/zentrale/skills/* ~/.claude/skills/
```
Arbeit des Mac-Agenten auf einem eigenen Zweig (`git switch -c mac-<thema>`), nicht direkt auf `main`.
