# 4 · MCP (30 min)

**Ziel:** Copilot benutzt Tools von außen – einen fertigen Remote-Server und den MCP-Server dieses Repos.

## Aufwärmen – Remote-Server (5 min)

1. `.vscode/mcp.json` öffnen. Über `deepwiki` erscheint **Start** → klicken. (Alternativ: Befehl **MCP: List Servers**.)
2. Agent-Chat:
   ```
   Erkläre mir mit deepwiki, wie Dependency Injection in fastapi/fastapi funktioniert.
   ```
   Tool-Aufruf bestätigen. Antwort mit Quelle prüfen.

## Hauptteil – eigener Server (20 min)

3. App läuft auf Port 8000. Zweites Terminal:
   ```powershell
   .venv\Scripts\python.exe mcp_server\server.py
   ```
   Erwartet: `Toolshed MCP läuft auf http://127.0.0.1:8001/mcp`.
4. In `mcp.json` den Server `toolshed` starten. Im Chat das Werkzeug-Symbol öffnen → Tools `list_items`, `list_overdue_loans`, `create_loan` … sind sichtbar.
5. Ausprobieren, Tool-Aufrufe und Parameter im Chat beobachten:
   ```
   Welche Geräte sind überfällig und bei wem?
   ```
   ```
   Leih den Beamer an Aylin Kaya aus, Rückgabe nächsten Freitag.
   ```
   ```
   Gib Ausleihe 1 zurück und zeig mir danach die offenen Ausleihen.
   ```
   Log im Server-Terminal mitlesen.
6. Prompt des Servers nutzen: `/mcp.toolshed.weekly_report`

## Bonus (5 min)

7. Neues Tool `member_summary(member_id)` in `mcp_server/server.py` (Person plus ihre Ausleihen) – mit Copilot bauen. Server neu starten, Befehl **MCP: Reset Cached Tools**, testen.

**Diskussion:** Übung 3 (Skill mit Skript) und Übung 4 (MCP) sprechen dieselbe API an. Wann ist was sinnvoll?

**Wenn es klemmt**
- Server startet nicht in VS Code → **MCP: List Servers** → **Show Output**.
- Fehlermeldung zu Richtlinien → Richtlinie „MCP servers in Copilot“ (Admin).
- Port 8001 belegt → `$env:TOOLSHED_MCP_PORT=8002` setzen, URL in `mcp.json` anpassen.
