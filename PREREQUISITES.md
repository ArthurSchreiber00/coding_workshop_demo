# Voraussetzungen für den Workshop

Bitte **vor** dem Workshop prüfen. Alles muss auf dem Laptop laufen, mit dem ihr teilnehmt.

## Teilnehmende

1. **VS Code** aktuell (mindestens 1.109, besser die neueste Version) mit den Erweiterungen **GitHub Copilot** und **GitHub Copilot Chat**, angemeldet mit dem Firmen-Copilot-Account.
   Test: Copilot Chat öffnen (`Ctrl+Alt+I`), im Dropdown unten „Agent“ und „Plan“ auswählen können.
2. **Python 3.11 oder neuer** (mindestens 3.10) mit `pip`. Test in PowerShell: `py -3 --version`
   Ihr müsst ein virtuelles Environment anlegen und diese Pakete installieren können (Versionen stehen in `requirements.txt`): `fastapi`, `uvicorn`, `jinja2`, `python-multipart`, `httpx`, `pytest`, `mcp`.
   Test:
   ```powershell
   py -3 -m venv C:\temp\venv-test
   C:\temp\venv-test\Scripts\python.exe -m pip install fastapi uvicorn jinja2 python-multipart httpx pytest mcp
   ```
3. **Git für Windows**. Test: `git --version`. Zugriff auf github.com zum Klonen des Übungs-Repos.
4. Netzwerk: lokale Ports 8000 und 8001 dürfen von VS Code erreicht werden; ausgehend HTTPS zu `mcp.deepwiki.com` und `learn.microsoft.com` (für den MCP-Teil).

## Administration (Copilot-Richtlinien im GitHub-Enterprise)

1. Richtlinie **„MCP servers in Copilot“** muss **aktiviert** sein (Standard: aus). Ohne sie funktioniert der MCP-Teil nicht.
2. Falls **„Restrict MCP access to registry servers“** genutzt wird: nicht auf „Registry only“ stellen, sonst ist der lokale MCP-Server blockiert. Ebenso VS-Code-Geräterichtlinien (`ChatMCP`, `ChatAllowedMcpServers`) prüfen.
3. Welche **Modelle** sind freigegeben? Für Plan Mode und den Review-Orchestrator ist ein starkes Modell (z. B. aktuelle Claude- oder GPT-Modelle) hilfreich.
4. Agent Mode, Custom Agents und Agent Skills sind allgemein verfügbar und benötigen keine Preview-Freigabe.

Prüfung am Laptop: Befehlspalette → **Developer: Policy Diagnostics** zeigt wirksame Richtlinien.
