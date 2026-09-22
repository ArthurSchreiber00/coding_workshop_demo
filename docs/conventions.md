# Konventionen

## Kommandos

| Zweck | Kommando (Windows PowerShell) |
|---|---|
| Abhängigkeiten installieren | `.venv\Scripts\python.exe -m pip install -r requirements.txt` |
| App starten | `.venv\Scripts\python.exe -m uvicorn app.main:app --reload` |
| Tests | `.venv\Scripts\python.exe -m pytest -q` |
| MCP-Server starten | `.venv\Scripts\python.exe mcp_server\server.py` |

Unter macOS/Linux entsprechend `.venv/bin/python`.

## Datenbank & Migrationen

- SQLite, Datei `toolshed.db` im Projektordner (überschreibbar mit der Umgebungsvariable `TOOLSHED_DB`).
- Migrationen sind reine SQL-Dateien in `app/migrations/`, Benennung `NNN_kurzname.sql`, werden beim Start in Reihenfolge ausgeführt.
- **Eine committete Migration wird nie geändert.** Schemaänderung = neue Datei mit der nächsten Nummer.
- Migrationen müssen idempotent sein (`IF NOT EXISTS`, `INSERT OR IGNORE`).

## SQL

- Kein ORM (siehe ADR-001). SQL steht nur in `app/repositories/`.
- Immer Parameter-Platzhalter (`?`) verwenden, nie String-Formatierung.

## API

- JSON-API unter `/api/...`, Ressourcen im Plural (`/api/items`, `/api/loans`).
- Schreibende Endpunkte verlangen den Header `X-Api-Key`.
- Fehler haben immer die Form `{"error": {"code": "<snake_case>", "message": "<Text>"}}`.
- Request- und Response-Modelle in `app/schemas.py` (Pydantic).

## HTML-Seiten

- Jinja2-Templates in `app/templates/`, alle Seiten erben von `base.html`.
- UI-Texte auf Deutsch, Code und Bezeichner auf Englisch.
- Formulare werden serverseitig verarbeitet (POST → Redirect).

## Tests

- `pytest`, ein Testmodul pro Router (`tests/test_items.py` …).
- `tests/conftest.py` setzt `TOOLSHED_DB` auf eine temporäre Datei; Tests laufen nie gegen `toolshed.db`.
- Neue Endpunkte bekommen mindestens einen Test für den Erfolgs- und einen für den Fehlerfall.

## Sonstiges

- Keine neuen Abhängigkeiten ohne Rücksprache; Standardbibliothek bevorzugen (`csv`, `datetime`, `sqlite3`).
- Commit-Nachrichten auf Englisch, Imperativ, kurz.
