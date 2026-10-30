# Bachelorarbeit

- **Studiengang:** Wirtschaftsinformatik
- **Thema:** Vorhersage von Hotelstornierungen anhand vorhandener Buchungen (Data Mining und Machine Learning)
- **Status:** fertig geschrieben
- **Abgabe:** Dezember 2026 (genaues Datum: ___)

## Bis zur Abgabe
- [ ] Abgabedatum eintragen
- [ ] Letztes Korrekturlesen
- [ ] Druck und Bindung
- [ ] Abgabe

## Später nutzen
- Projekt fürs Portfolio und den Lebenslauf (ML und Datenanalyse)

## Ergänzt von Claude (2026-10-18)
- Deckblatt nennt als Abgabedatum den 01.12.2026.
- Einseitige Kurzfassung für Laien: `Desktop\Malik-BA\thesis\Thesis_auf_einen_Blick.pdf`
- Kernergebnis: realistisch F1 ≈ 0,76 / ROC-AUC ≈ 0,90 (HistGradientBoosting, zeitbasierter Split)

## Ergänzt von Claude (2026-10-19)
- Neue Feature-Analyse in `Desktop\Malik-BA\results\feature_analyse\` (Skripte `feature_vergleich.py`, `shap_analyse.py`).
- Korrelationsreduktion 29 → 24 Merkmale kostet bei allen Modellen etwas Güte (RF zufällig F1 0,851 → 0,839) → bisherige 29 Merkmale beibehalten.
- SHAP-Top-5 (RF): country, deposit_type, total_of_special_requests, market_segment, lead_time.
- [ ] Entscheiden, ob und wo die Analyse in die Thesis kommt (Kap. 4, Anhang?)

## Ergänzt von Claude (2026-10-22)
- Kapitel 6 (Fazit) neu geschrieben, mit roten `\tbd{…}`-Platzhaltern für die Zahlen aus dem neuen Optimierungslauf.
- Neuer, methodisch sauberer Optimierungslauf (`optimization/`) ist beim ersten Versuch abgestürzt (Windows-Prozesspool) und muss neu gestartet werden.
- [x] Optimierungslauf neu starten (repariert, fertig 18:33 nach 3,6 h)
- [ ] `\tbd` in Kapitel 6 ersetzen und Schwellen-Stellen (0,40/0,25) in Kap. 4/5, Kurzfassung, Abstract, Anhang korrigieren
- Ergebnis des sauberen Laufs: bestes Modell zeitbasiert XGBoost, F1 0,782 / ROC-AUC 0,905 (HGB praktisch gleichauf). Gewinn durch Tuning liegt im Bereich der Streuung → Kernaussage „Methodik wichtiger als letztes Prozent F1“ bestätigt.

## Ergänzt von Claude (2026-10-27)
- **Neues Abgabedatum: 11. Januar 2027** (laut Maliks Auftrag; Deckblatt steht noch auf 01.12.2026).
- `ba-optimierung` in `main` gemergt (5c376e7). Backup-Tag `stand-vor-ueberarbeitung`.
- Überarbeitung in 3 Phasen gestartet. Phase 1 (Audit) fertig: `Desktop\Malik-BA\docs\audit.md` (Commit 139b6b6).
- Hauptproblem: Kurzfassung, Kap. 4 und 5 nennen HGB 0,757, Kap. 6 nennt XGBoost 0,782 aus dem sauberen Lauf. Der saubere Lauf fehlt in Kap. 4 und in Tab. A.5.
- Neu entdeckt: `assigned_room_type` ist klarer Leakage (abweichendes Zimmer → nur 5 % Storno), `booking_changes` verdächtig.
- [ ] Entscheiden: Leakage-Merkmale aus dem Hauptmodell oder nur Sensitivitätsanalyse
- [ ] Phase 2 (Code) und Phase 3 (Thesis)

## Ergänzt von Claude (2026-10-28)
- [x] Leakage-Merkmale entschieden: `assigned_room_type` und `booking_changes` raus aus dem Hauptmodell, nur noch Sensitivität
- [x] Phase 2 (Code) fertig, Commit 066a00c. Abschließender Lauf neu auf 27 Merkmalen (2,75 h).
- Neues Ergebnis: bestes Modell **HistGradientBoosting**, OOF-Schwelle 0,38, Test-F1 **0,768** [0,762; 0,774], ROC-AUC 0,893. XGBoost statistisch gleichauf (p = 0,73).
- Fairer Duplikat-Test: kein Effekt (0,768 → 0,768). Die alte Aussage „−0,10 F1“ fällt weg.
- Leakage-Merkmale bringen +0,011 F1, also wenig. Merkmalsreduktion schadet HGB (−0,049).
- Alle alten → neuen Werte: `Desktop\Malik-BA\docs\alt_neu_werte.md`
- [ ] Phase 3 (Thesis überarbeiten), wartet auf „weiter“
- [ ] Phase 4 (Endkontrolle, Tag abgabe-kandidat-1)
- [x] Phase 3 (Thesis überarbeitet) fertig am 2026-10-28, Commit aea4ad7. Konsistenzprüfung: 0 abweichende Tabellenzahlen, 86 Seiten.
- Ablation: Verlust der reduzierten Merkmalsmenge kommt von `agent` und `arrival_date_year`. Alle 27 Merkmale bleiben.
- Kostenschwelle aus OOF bei 4:1: 0,17. Die OOF-Schwelle 0,38 entspricht etwa 1,6:1.
- [ ] Malik: neue Quellen prüfen (efron1993, dietterich1998, lundberg2020, zadrozny2003, gama2014), Screenshot der App neu, Deckblatt/Erklärung mit HS-Vorlage abgleichen
- [ ] Phase 4 (Endkontrolle, Tag abgabe-kandidat-1), wartet auf „weiter“
- [x] Phase 4 (Endkontrolle) fertig am 2026-10-28, Commit 1b8caee, Tag **abgabe-kandidat-1** gepusht. Änderungsprotokoll: `Desktop\Malik-BA\docs\aenderungsprotokoll.md`.
- `arrival_date_year`: ohne das Jahr F1 0,742 (−0,026). Merkmal bleibt, wirkt aber als Drift-Indikator (Testmenge nur 2017) → im Einsatz regelmäßig neu trainieren.
- Umfang Kapitel 1–6: 64 Seiten (Ziel 60), Kürzungsvorschläge liegen vor, noch nichts gekürzt.
- [ ] Malik: entscheiden, ob und wo gekürzt wird
- [x] 2026-10-28: Kurzfassung (Maliks Text) und Abstract neu, je eine Seite. Kürzungen 4.5, SHAP-Abbildungen in den Anhang, 6.1/6.3 gestrafft → Kapitel 1–6: 62 Seiten (Commit 3699331, noch nicht gepusht, Tag abgabe-kandidat-1 zeigt auf den Stand davor).
- [x] 2026-10-28: Tag **abgabe-kandidat-2** (Commit 0c3b7e5) gepusht. 62 Seiten bleiben, keine weitere Kürzung. Kurzfassung/Abstract je eine Seite.
- [x] 2026-10-28: Tag **abgabe-kandidat-3** (Commit 3df154e) gepusht.
- [x] 2026-10-28: App-Screenshot für Anhang A.4 automatisch erzeugt (`code/make_app_screenshot.py`, echte Testbuchung, 77,5 % > 0,38). Tag **abgabe-kandidat-4** (Commit 24b9ca6) gepusht. Offen nur noch: Quellen prüfen, Deckblatt/Erklärung mit HS-Vorlage abgleichen, ENTWURF-Kommentare.
- [x] 2026-10-28: Prototyp verbessert (Anreisedatum statt Monat, Dezimalkomma, Standardwert company = keine Firma). App rechnet jetzt exakt wie das Modell (Beispielbuchung 73,0 %). Tag **abgabe-kandidat-5** (Commit d9e876d) gepusht.
