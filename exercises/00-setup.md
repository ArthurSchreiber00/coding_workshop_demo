# 0 · Setup (15 min)

**Ziel:** App läuft lokal, Tests sind grün, Copilot ist bereit.

1. Repo klonen und öffnen:
   ```powershell
   git clone <REPO-URL> toolshed
   cd toolshed
   code .
   ```
2. Environment und Abhängigkeiten (ausführlich mit Kontrollen: [QUICKSTART.md](../QUICKSTART.md)):
   ```powershell
   py -3 -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
3. App starten und im Browser öffnen: http://127.0.0.1:8000 (Oberfläche) und http://127.0.0.1:8000/docs (API):
   ```powershell
   .venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```
4. Tests in einem zweiten Terminal:
   ```powershell
   .venv\Scripts\python.exe -m pytest
   ```
   Erwartet: `23 passed`.
5. Copilot prüfen: Chat öffnen (`Ctrl+Alt+I`). Im Dropdown unten stehen **Agent** und **Plan**. Ein Modell auswählen.
6. 5 Minuten durch den Code klicken: `app/main.py`, `app/routers/`, `docs/architecture.md`.

**Wenn es klemmt**
- `py` nicht gefunden → `python -m venv .venv`.
- VS Code fragt nach dem Python-Interpreter → `.venv\Scripts\python.exe` wählen.
- Port 8000 belegt → `--port 8080` anhängen (dann auch in den späteren Übungen).
