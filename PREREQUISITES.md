# Voraussetzungen für den Workshop

Bitte **vor** dem Workshop prüfen. Alles muss auf dem Laptop laufen, mit dem ihr teilnehmt.

## Teilnehmende

1. **VS Code** aktuell (mindestens 1.109, besser die neueste Version) mit den Erweiterungen **GitHub Copilot** und **GitHub Copilot Chat**, angemeldet mit dem Firmen-Copilot-Account.
   Test: Copilot Chat öffnen (`Strg+Alt+I`), im Dropdown unten „Agent“ und „Plan“ auswählen können.
2. **Python 3.11 oder neuer** (mindestens 3.10) mit `pip`. Test in PowerShell: `py -3 --version`
   Ihr müsst ein virtuelles Environment anlegen und diese Pakete installieren können (Versionen stehen in `requirements.txt`): `fastapi`, `uvicorn`, `jinja2`, `python-multipart`, `httpx`, `pytest`, `mcp`.
   Test:
   ```powershell
   py -3 -m venv C:\temp\venv-test
   C:\temp\venv-test\Scripts\python.exe -m pip install fastapi uvicorn jinja2 python-multipart httpx pytest mcp
   ```
3. **Git für Windows**. Test: `git --version`. Zugriff auf github.com zum Klonen des Übungs-Repos.
4. Netzwerk: lokale Ports 8000 und 8001 dürfen von VS Code erreicht werden; ausgehend HTTPS zu `mcp.deepwiki.com` (für den MCP-Teil).
