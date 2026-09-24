# 2 · Plan Mode (30 min)

**Ziel:** Ein Feature planen lassen, den Plan lesen und steuern, dann umsetzen lassen.

**Feature „Überfällige Ausleihen“:** Seite `/loans/overdue` mit allen überfälligen Ausleihen, Zähler in der Navigation, `GET /api/loans/overdue`, Tests.

1. Neuer Chat, Dropdown → **Plan**. Eher starkes Modell wählen.
2. Das Feature in eigenen Worten beschreiben. Tipp: bewusst knapp anfangen und schauen, welche Rückfragen kommen. Rückfragen beantworten oder Copilot nach den Mustern des Repos entscheiden lassen.
3. Plan lesen: **Steps**, **Relevant files**, **Verification**, **Decisions**
4. Einmal nachschärfen, z. B. im Chat mehr Tests fordern, sodass der Plan erweitert wird.
5. Schwächeres Modell auswählen und **Start Implementation** klicken. Zusehen, bei Bedarf eingreifen. Danach:
   ```powershell
   .venv\Scripts\python.exe -m pytest
   ```
   Die App läuft aus dem Setup weiter und hat die Änderungen schon übernommen (sonst neu starten). Seite http://127.0.0.1:8000/loans/overdue öffnen.
6. Zum Vergleich: Wie hätte ein präziser erster Prompt ausgesehen (Route, Sortierung, Tests, Grenzen)? Welche Rückfragen hätte er erspart?
