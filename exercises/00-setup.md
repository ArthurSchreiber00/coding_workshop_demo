# 0 · Setup (15 min)

**Ziel:** App läuft lokal, Tests sind grün, Copilot ist bereit.

1. Repo klonen und öffnen:
   ```powershell
   git clone https://github.com/ArthurSchreiber00/coding_workshop_demo.git toolshed
   cd toolshed
   code .
   ```
2. Environment und Abhängigkeiten (ausführlich mit Kontrollen: QUICKSTART.md im Repo):
   ```powershell
   py -3 -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
3. App starten und im Browser öffnen: http://127.0.0.1:8000 (Oberfläche) und http://127.0.0.1:8000/docs (API):
   ```powershell
   .venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```
   Das Terminal bleibt offen. Dank `--reload` übernimmt die App spätere Codeänderungen selbst.
4. Tests in einem zweiten Terminal:
   ```powershell
   .venv\Scripts\python.exe -m pytest
   ```
   Erwartet: `28 passed`.
5. Interpreter wählen: Befehlspalette (`Strg+Shift+P`) → **Python: Select Interpreter** → `.venv\Scripts\python.exe`. Damit startet Copilot in den späteren Übungen Tests mit dem richtigen Python.
6. Copilot prüfen: Chat öffnen (`Strg+Alt+I`). Im Dropdown unten stehen **Agent** und **Plan**. Ein Modell auswählen.
7. 5 Minuten durch den Code klicken: `app/main.py`, `app/routers/`, `docs/architecture.md`.

**Wenn es klemmt**
- `py` nicht gefunden → `python -m venv .venv`.
- `.venv` wird bei Schritt 5 nicht angeboten → „Enter interpreter path“ → `.venv\Scripts\python.exe`.
- Port 8000 belegt → `--port 8080` anhängen und in den späteren Übungen `8080` statt `8000` verwenden.
