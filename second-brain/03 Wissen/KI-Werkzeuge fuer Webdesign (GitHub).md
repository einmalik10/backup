# KI-Werkzeuge für Webdesign (GitHub)

- **Quelle:** 12 GitHub-Repos, die Malik am 2026-10-27 gesammelt hat, gelesen und bewertet von Claude
- **Bereich:** Tech / Webdesign / Verkaufen

## Kernaussage in einem Satz
- Nicht alles installieren: Nur was direkt eine Website, einen Lead oder ein Video besser macht, kommt rein, und Fremd-Plugins werden vor der Installation gelesen, weil sie mit vollen Rechten laufen.

## Bewertung

| Repo | Was es ist | Nutzen für mich | Kosten / Voraussetzung | Stufe |
|---|---|---|---|---|
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 25 Arbeitsabläufe für KI-Agenten (u. a. Frontend-UI, Performance, Barrierefreiheit, Browser-Tests, Launch) | Websites sauberer bauen und prüfen, Lighthouse-Werte hoch | kostenlos, MIT | **A: jetzt** |
| [anthropics/…/claude-security](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-security) | Offizielles Sicherheits-Review mit mehreren Agenten, Bericht + Patch-Vorschläge | Formulare (anfrage.php), Repo und Kundenseiten vor Livegang prüfen | kostenlos, Python 3.9+ | **A: jetzt** |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | HTML/CSS → MP4-Video, für Agenten gebaut | MI Visuals: Reels, Vorher/Nachher-Videos für Mappen und Instagram | kostenlos, Apache 2.0, braucht Node 22+ und **FFmpeg** | **A: jetzt** |
| [every-app/open-seo](https://github.com/every-app/open-seo) | Eigenes SEO-Tool (Keywords, Ranking, Site-Audit, Backlinks) statt Semrush/Ahrefs, mit MCP | SEO als Zusatzleistung verkaufen, Ranking der Kunden belegen | DataForSEO-Konto (Pay-as-you-go), Hosting auf eigenem Cloudflare möglich | **B: mit Budget** |
| [apify/apify-mcp-server](https://github.com/apify/apify-mcp-server) | Zugriff auf tausende Scraper (Google Maps, Instagram, Bewertungen) | Leads mit Bewertungen und Social-Profilen anreichern | Apify-Konto, Kosten pro Lauf | **B: mit Budget** |
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | `gws`: Gmail, Drive, Kalender, Sheets per Befehl (inoffiziell) | Angebots-Tabellen, Termine, Ablage | Google-Cloud-Projekt + OAuth, aufwendig; nie Werbe-Mails ohne Ja (§ 7 UWG) | **B: später** |
| [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Browser-Steuerung als Befehl + Skill für Agenten | Klicktests; meine Python-Playwright-Skripte decken das meiste schon ab | kostenlos, npm | **C: bei Bedarf** |
| [nateherkai/scroll-craft](https://github.com/nateherkai/scroll-craft) | Skill für „premium“ Scroll-Websites mit Video-Scrubbing | Nur für Show-Demos oder MI Visuals; für Läden oft zu viel | kostenlos, FFmpeg, Einzelautor, vorher lesen | **C: testen** |
| [blader/humanizer](https://github.com/blader/humanizer) | Macht KI-Texte menschlicher | Beispiele nur Englisch, für deutsche Texte unklar | kostenlos | **C: testen** |
| [stripe/…/stripe-best-practices](https://github.com/stripe/ai/tree/main/skills/stripe-best-practices) | Regeln für Stripe-Zahlungen | Erst wenn ein Kunde online bezahlen lässt (nicht Shopify) | kostenlos | **C: bei Bedarf** |
| [supabase/agent-skills](https://github.com/supabase/agent-skills) | Skills für Supabase-Datenbank | Erst für Apps/CRM mit Datenbank (Stempelkarte, Kundenkonto) | kostenlos, Supabase-Konto | **C: bei Bedarf** |
| [expo/skills](https://github.com/expo/skills) | Skills für Handy-Apps mit Expo/React Native | Erst wenn ich echte App-Store-Apps baue | kostenlos, EAS teils kostenpflichtig | **C: bei Bedarf** |

## Wie wende ich das an?
- Stufe A zuerst, dann eine echte Kundenseite damit prüfen und schauen, ob es wirklich besser wird.
- Stufe B nur mit festem Monatsbudget und erst, wenn ein Kunde dafür zahlt (SEO-Paket, Lead-Anreicherung).
- Fremd-Plugins (Einzelautoren) vorher lesen: SKILL.md, Skripte und vor allem Hooks. Sie laufen mit meinen Rechten.
- Design-Skills (z. B. scroll-craft) nie direkt auf eine Live-Kundenseite loslassen: erst Entwurf zeigen, dann bauen.

## Umgesetzt (2026-10-27)
- **addyosmani/agent-skills**: geprüft (Hooks liegen im Repo, sind aber nicht im Plugin eingetragen, wurden nicht übernommen). Eingebaut als Skills in `~/.claude/skills`: `frontend-ui-engineering`, `performance-optimization`, `browser-testing-with-devtools`, `security-and-hardening`, `shipping-and-launch`, `code-review-and-quality`, dazu die Checklisten in `agent-skills-references` (nur Pfade angepasst).
- **HyperFrames**: geprüft (keine Hooks, CLI ohne Installations-Skripte, anonyme Nutzungsdaten → abgeschaltet). Eingebaut: Skills `hyperframes` und `hyperframes-cli`, CLI `hyperframes@0.8.209` global. Weggelassen: `media-use` (HeyGen/Gemini), figma, registry, remotion, slideshow.
- **FFmpeg 9.0.2** per winget (nur für Malik, ohne Admin).
- Rendern nutzt den vorhandenen Playwright-Chrome (`PRODUCER_HEADLESS_SHELL_PATH`). Testvideo 3 s, 1080p, Einblendung funktioniert.
- Nicht ausführen: `npx hyperframes skills update` (lädt die weggelassenen Skills ungeprüft nach).
- Video starten: im Chat „mach ein Video mit HyperFrames …“, die Skills übernehmen den Rest.
- 2026-10-27: Die 8 Skills liegen zusätzlich im Repo `xaloH/webdesign-beginner` unter `.claude/skills/` (Commit 67cdb8b, gepusht). Wer das Repo klont, hat sie automatisch. FFmpeg und `hyperframes@0.8.209` muss jeder selbst installieren (steht in der README).

## CapCut (geprüft 2026-10-27)
- Gut für schnellen Schnitt am Handy/PC: automatische Untertitel, Hintergrund entfernen, Vorlagen. Pro-Abo, Preise schwanken je nach Gerät (ca. 9–20 €/Monat), vor Abschluss im App-Store prüfen.
- **Für Kunden-Werbung aufpassen:** Nur Material mit Kennzeichnung „commercial use“ verwenden, Musik aus der Bibliothek ist laut Berichten oft nicht für Werbung freigegeben → eigene lizenzierte Musik. Die Nutzungsbedingungen geben CapCut weitgehende Rechte an hochgeladenen Inhalten (strittig seit Juni 2025) → bei Kundenvideos mit Gesichtern vorher klären.
- **Keine offizielle Schnittstelle.** Claude geht nur über inoffizielle MCP-Server, die CapCut-Projektdateien bearbeiten (CapCut dabei schließen, kann bei Updates brechen). Obsidian: keine direkte Verbindung, aber Skripte, Shotlists und Ideen als Notizen.
- Arbeitsteilung: Claude schreibt Skript und Untertitel → HyperFrames für Text-/Motion-Werbung → CapCut für den Schnitt von echtem Filmmaterial.

## Animierte Scroll-Websites (Instagram-Trend, geprüft 2026-10-28)
- **Was verkauft wird:** Prompt-Sammlungen für „3D-/Scroll-Websites“, z. B. scrolltide.co für 299 $ einmalig (React, Next.js, GSAP, Three.js, Shader, Lenis). Accounts verkaufen pro Branche (Burger-Restaurant, Fotograf, Autohaus) „Prompt + Workflow“ gegen Kommentar/DM.
- **Das Rezept dahinter:** KI-Video oder eigenes Video (z. B. Burger wird gepresst, Auto dreht sich) → in Einzelbilder zerlegen (FFmpeg) → beim Scrollen Bild für Bild abspielen, dazu große Typo, fixierte Abschnitte, Text-Einblendungen. Ein Kommentar dazu: „fal.ai + Claude Code, 50 Cent, 3 Minuten“.
- **Kritik in den Kommentaren:** schlecht lesbarer Text, zu viel Scrollen. → Lesbarkeit und Handy zuerst.
- **scroll-craft geprüft:** keine Hooks, Engine reines JavaScript ohne Abhängigkeiten und ohne Fremdserver (gut für DSGVO), Vorschau-Server nur lokal. Einziger Netzaufruf: `kie.mjs` zu kie.ai (kostenpflichtige KI-Bilder/Videos, nur mit eigenem Schlüssel). Prüft Kontrast, Bewegung und Barrierefreiheit per Screenshots.
- **Mein Vorteil:** eigene Aufnahmen über MI Visuals statt KI-Videos, die alle gleich aussehen.
- 2026-10-28: scroll-craft als Skill in `~/.claude/skills/scroll-craft` installiert (ohne Plugin-Hülle, mit QUELLE.md). Technik-Check grün (Node, FFmpeg, Chrome). Ablauf des Skills: erst Briefing mit 8 Fragen, dann Material, dann bauen und per Screenshots prüfen.

## kie.ai (KI-Bilder und -Videos, 2026-10-28)
- Prepaid-Guthaben, kein Abo. 1 Credit ≈ 0,005 $ (laut Drittquellen, im Dashboard prüfen).
- scroll-craft nutzt: Standbild `seedream/5-pro` ≈ 28 Credits (~0,14 $), Video `kling/v2-1-pro` 5 s ≈ 160 Credits (~0,80 $). Demo mit ~6 Bildern + 2 Clips ≈ 500 Credits (~2,50 $), mit Neuversuchen 5–10 $ einplanen.
- Schlüssel liegt nur in `webdesign/arbeit/scrollcraft/.env` (von Git ignoriert). Nie in Chat oder Repo.
- Für echte Kunden lieber eigene Aufnahmen; KI nur für Demos und Stimmungsbilder.

## Higgsfield vs. kie.ai (2026-10-28)
- **Higgsfield:** Web-Oberfläche mit vielen Modellen (Kling, Veo, Seedance u. a.) und Kamera-Vorlagen („Cinema Studio“). Abo laut Drittquellen ab ca. 19 $/Monat, kommerzielle Nutzung nur in bezahlten Tarifen. Öffentliche API in der Recherche nicht gefunden → von Hand erzeugen, Dateien in den Projektordner legen.
- **kie.ai:** Prepaid ohne Abo, per API, direkt in scroll-craft eingebaut → Claude kann automatisch erzeugen und neu versuchen.
- Gleiche Modelle dahinter. Higgsfield = mehr Komfort und Kamera-Effekte beim Selbermachen, kie.ai = automatisierbar und günstig für Demos.
