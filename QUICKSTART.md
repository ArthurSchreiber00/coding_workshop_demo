# Quick Start (Windows)

Repository installieren, starten und prüfen – in fünf Minuten.

## Voraussetzungen

- Windows 10/11, **PowerShell** (vorinstalliert)
- **Python 3.11 oder neuer** (mindestens 3.10) – Test: `py -3 --version`
- **Git** – Test: `git --version`
- Internetzugang zu github.com und pypi.org

## Weg A: ein Befehl

```powershell
git clone <REPO-URL> toolshed
cd toolshed
.\quickstart.cmd
```

Das Skript sucht Python, legt `.venv` an, installiert die Abhängigkeiten, führt die Tests aus, startet die App in einem eigenen Fenster, wartet bis sie antwortet, prüft die Startseite und öffnet den Browser.

Erwartete Ausgabe am Ende:

```
    OK      Website läuft: http://127.0.0.1:8000  (10 Geräte in der API)
    OK      Startseite rendert (Toolshed / Übersicht)
```

Optionen: `.\quickstart.cmd -SkipTests` · `-Port 8080` · `-NoBrowser` · `-CheckOnly` (nur prüfen, ob die Website läuft).

## Weg B: von Hand

```powershell
git clone <REPO-URL> toolshed
cd toolshed
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

## Prüfen, ob die Website läuft

- Browser: http://127.0.0.1:8000 zeigt die Seite **Übersicht** mit 10 Geräten und 5 Personen; http://127.0.0.1:8000/docs zeigt die API-Dokumentation.
- PowerShell (zweites Fenster):
  ```powershell
  Invoke-WebRequest http://127.0.0.1:8000/api/items -UseBasicParsing | Select-Object StatusCode
  ```
  Erwartet: `StatusCode 200`.
- Oder: `.\quickstart.cmd -CheckOnly`

## Stoppen und zurücksetzen

- Stoppen: Server-Fenster schließen oder `Strg+C` im Terminal.
- Datenbank zurücksetzen: App stoppen, `toolshed.db` löschen, App neu starten (Demodaten werden neu angelegt).

## Wenn es klemmt

| Symptom | Lösung |
|---|---|
| `py` wird nicht erkannt | Python von python.org installieren und „Add python.exe to PATH“ anhaken – oder `python` statt `py -3` verwenden. |
| `python` öffnet den Microsoft Store | Einstellungen → Apps → Erweiterte App-Einstellungen → App-Ausführungsaliase: `python.exe` und `python3.exe` ausschalten. Oder `py -3` verwenden. |
| „Die Ausführung von Skripts ist auf diesem System deaktiviert“ | `.\quickstart.cmd` statt `.\quickstart.ps1` verwenden (umgeht die Execution Policy nur für diesen Aufruf). Alternativ Weg B. |
| `pip install` scheitert (Timeout, SSL, 407) | Firmenproxy: vorher `$env:HTTPS_PROXY = "http://proxy:port"` setzen. Interner PyPI-Spiegel: `pip config set global.index-url <URL>`. |
| Port 8000 belegt | `.\quickstart.cmd -Port 8080` bzw. `--port 8080` an uvicorn anhängen. |
| VS Code findet den Interpreter nicht | Befehlspalette → **Python: Select Interpreter** → `.venv\Scripts\python.exe`. |
| Tests rot | Ausgabe lesen; meist fehlende Abhängigkeiten → `pip install -r requirements.txt` wiederholen. |

macOS/Linux: `python3 -m venv .venv`, `.venv/bin/python` statt `.venv\Scripts\python.exe`; das Skript läuft dort mit `pwsh ./quickstart.ps1`.
