# 4 · MCP (30 min)

**Ziel:** Copilot benutzt Tools von außen – einen fertigen Remote-Server und den MCP-Server dieses Repos.

## Aufwärmen – Remote-Server (5 min)

1. `.vscode/mcp.json` öffnen. Über `deepwiki` erscheint **Start** → klicken. (Alternativ: Befehl **MCP: List Servers**.)
2. Im Agent-Chat mit deepwiki herausfinden, wie man im aktuellen MCP Python SDK ein Tool als read-only markiert. Das Repo auf GitHub heißt `modelcontextprotocol/python-sdk`. Tool-Aufruf bestätigen. Erwartet: `@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))`.

## Hauptteil – eigener Server (20 min)

3. App läuft auf Port 8000. Weiteres Terminal:
   ```powershell
   .venv\Scripts\python.exe mcp_server\server.py
   ```
   Erwartet: `Toolshed MCP läuft auf http://127.0.0.1:8001/mcp`.
4. In `mcp.json` den Server `toolshed` starten. Im Chat das Einstellungs-Symbol öffnen → Tools `list_items`, `list_overdue_loans`, `create_loan` … sind sichtbar.
5. Die App über den Chat steuern und dabei Tool-Aufrufe und Parameter beobachten:
   - überfällige Ausleihen abfragen, mit Person
   - ein freies Gerät an eine Person verleihen, mit Rückgabedatum
   - diese Ausleihe wieder zurückbuchen und danach die offenen Ausleihen anzeigen
   Log im Server-Terminal mitlesen. Auffällig: Jeder Aufruf will bestätigt werden, auch reine Abfragen.
6. Prompt des Servers nutzen: `/mcp.toolshed.weekly_report`

## Bonus

7. Im Chat aus dem Aufwärmen Copilot alle Tools in `mcp_server/server.py`, die nichts verändern, als read-only markieren lassen.
   Server im Terminal mit `Strg+C` stoppen und neu starten. Dann **MCP: List Servers** → `toolshed` → **Restart** und Befehl **MCP: Reset Cached Tools**.
   Erwartet: Abfragen laufen ohne Bestätigung, Ausleihe und Rückgabe fragen weiter nach.

**Diskussion:** Übung 3 (Skill mit Skript) und Übung 4 (MCP) sprechen dieselbe API an. Wann ist was sinnvoll? Und wann lohnt ein Doku-Server wie DeepWiki, wann nicht?
