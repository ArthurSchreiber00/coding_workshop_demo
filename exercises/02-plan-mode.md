# 2 · Plan Mode (30 min)

**Ziel:** Ein Feature planen lassen, den Plan lesen und steuern, dann umsetzen lassen.

**Feature „Überfällige Ausleihen“:** Seite `/loans/overdue` mit allen überfälligen Ausleihen, Zähler in der Navigation, `GET /api/loans/overdue`, Tests.

1. Neuer Chat, Dropdown → **Plan**. Stärkstes verfügbares Modell wählen.
2. Prompt, absichtlich knapp:
   ```
   Wir brauchen eine Übersicht der überfälligen Ausleihen.
   ```
   Copilot stellt Rückfragen. Beantworten – oder: „Entscheide nach den Mustern dieses Repos.“
3. Plan lesen: **Steps**, **Relevant files**, **Verification**, **Decisions**. Prüfen: Router dünn? Kein SQL im Router? Fehlerformat? Ein Test pro Fall? Nichts an bestehenden Migrationen geändert?
4. Einmal nachschärfen, z. B.:
   ```
   Sortiere nach Tagen überfällig, absteigend. Ergänze einen Test für den Fall „keine überfälligen Ausleihen“.
   ```
5. **Start Implementation** klicken. Zusehen, bei Bedarf eingreifen. Danach:
   ```powershell
   .venv\Scripts\python.exe -m pytest
   ```
   App starten, Seite öffnen.
6. Zum Vergleich: Wie hätte ein präziser Prompt ausgesehen (Route, Sortierung, Tests, Grenzen)? Was hätte er an Rückfragen gespart?

**Wenn es klemmt**
- Kein **Plan** im Dropdown → VS Code und Copilot-Chat-Erweiterung aktualisieren.
- Plan verschwunden → **Open in Editor** direkt nach dem Plan nutzen, oder Befehl **Chat: Show Memory Files**.
- Umsetzung dauert zu lang → Zeitbox einhalten, den Rest per Prompt „Nur die API-Route und ihre Tests umsetzen“ eingrenzen.
