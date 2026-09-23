# Toolshed

Kleine Web-App zur Geräteausleihe im Team – das Übungsprojekt für den Workshop **KI-Coding**.


Die Codebasis ist absichtlich nicht perfekt. Was du findest, gehört vermutlich zum Workshop.

## Schnellstart (Windows, PowerShell)

Schritt für Schritt mit Kontrollen und Hilfe bei Problemen: [QUICKSTART.md](QUICKSTART.md). Kurzfassung:

```powershell
git clone <REPO-URL> toolshed
cd toolshed
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

- Oberfläche: http://127.0.0.1:8000
- API-Dokumentation (OpenAPI): http://127.0.0.1:8000/docs

macOS/Linux: `python3 -m venv .venv` und `.venv/bin/python` statt `.venv\Scripts\python.exe`.

Beim ersten Start wird `toolshed.db` angelegt und mit Demodaten gefüllt (`app/migrations/`). Zum Zurücksetzen die Datei löschen.

## Übungen

Die Aufgaben für den Workshop stehen in [`exercises/`](exercises/README.md). Voraussetzungen: [`PREREQUISITES.md`](PREREQUISITES.md).

## Struktur

```
app/
  main.py            FastAPI-App, Router, Migrationen beim Start
  config.py          Konfiguration
  db.py              SQLite-Verbindung, Migrationen
  migrations/        NNN_name.sql – neue werden beim Start einmalig angewendet
  routers/           HTTP-Schicht: pages.py (HTML), items/members/loans/reports (JSON unter /api)
  repositories/      Datenzugriff (SQL)
  schemas.py         Pydantic-Modelle
  templates/         Jinja2-Templates
  static/            CSS, JS, Logo
tests/               pytest (eigene Test-DB, nie toolshed.db)
mcp_server/          MCP-Server über die API (Streamable HTTP, Port 8001)
docs/                Architektur, Konventionen, ADRs
exercises/           Workshop-Aufgaben
```

## API

Lesende Endpunkte sind offen, schreibende verlangen den Header `X-Api-Key` (Wert siehe `app/config.py`). Fehler kommen immer als

```json
{"error": {"code": "item_not_found", "message": "Gerät 42 existiert nicht."}}
```

## MCP-Server

```powershell
.venv\Scripts\python.exe mcp_server\server.py
```

läuft auf `http://127.0.0.1:8001/mcp` und ist in `.vscode/mcp.json` als Server `toolshed` eingetragen. Voraussetzung: die App läuft auf Port 8000. Test ohne VS Code: `.venv\Scripts\python.exe mcp_server\smoke_test.py`.

Weiteres: [docs/architecture.md](docs/architecture.md), [docs/conventions.md](docs/conventions.md)
