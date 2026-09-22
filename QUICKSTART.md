# Quick Start (Windows)

Alle Befehle werden in **PowerShell** eingegeben (Startmenü → „PowerShell“, oder in VS Code: Terminal → Neues Terminal). Nach jedem Schritt steht, woran du erkennst, dass er geklappt hat.

## 1. Voraussetzungen prüfen

```powershell
py -3 --version
git --version
```

Erwartet: `Python 3.11.x` oder neuer (mindestens 3.10) und `git version 2.x`.

## 2. Repository holen

```powershell
git clone <REPO-URL> toolshed
cd toolshed
```

Erwartet: ein Ordner `toolshed` mit `app`, `tests`, `exercises`, `requirements.txt`.

Optional VS Code öffnen: `code .`

## 3. Virtuelles Environment anlegen

```powershell
py -3 -m venv .venv
```

Kontrolle:

```powershell
Test-Path .venv\Scripts\python.exe
```

Erwartet: `True`.

## 4. Abhängigkeiten installieren

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Erwartet: letzte Zeile beginnt mit `Successfully installed` (beim zweiten Mal `Requirement already satisfied`). Dauer: etwa eine Minute.

## 5. Tests ausführen

```powershell
.venv\Scripts\python.exe -m pytest
```

Erwartet: `24 passed`.

## 6. App starten

```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Erwartet:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Das Fenster bleibt offen. Die App läuft, solange es offen ist. Beim ersten Start wird `toolshed.db` mit Demodaten angelegt.

## 7. Prüfen, ob die Website läuft

Im Browser:

- http://127.0.0.1:8000 → Seite **Übersicht** mit 10 Geräten und 5 Personen
- http://127.0.0.1:8000/docs → API-Dokumentation (Swagger UI)

Oder in einem **zweiten** PowerShell-Fenster:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/api/items -UseBasicParsing | Select-Object StatusCode
```

Erwartet: `StatusCode 200`.

```powershell
((Invoke-WebRequest http://127.0.0.1:8000/api/items -UseBasicParsing).Content | ConvertFrom-Json).Count
```

Erwartet: `10` (Anzahl Geräte in der API).

## 8. VS Code auf das Environment zeigen

Befehlspalette (`Strg+Shift+P`) → **Python: Select Interpreter** → `.venv\Scripts\python.exe` wählen. Danach funktionieren Tests und Ausführen aus VS Code heraus.

## Stoppen und zurücksetzen

- Stoppen: `Strg+C` im Fenster, in dem die App läuft.
- Demodaten zurücksetzen: App stoppen, dann `Remove-Item toolshed.db`, dann App neu starten.

## Wenn es klemmt

| Symptom | Lösung |
|---|---|
| `py` wird nicht erkannt | `python` statt `py -3` verwenden. Falls auch das fehlt: Python von https://www.python.org/downloads/ installieren, dabei „Add python.exe to PATH“ anhaken, PowerShell neu öffnen. |
| `python` öffnet den Microsoft Store | Einstellungen → Apps → Erweiterte App-Einstellungen → App-Ausführungsaliase: `python.exe` und `python3.exe` ausschalten. Oder `py -3` verwenden. |
| `pip install` zeigt `[notice] A new release of pip is available` | Kein Fehler, nur ein Hinweis. Ignorieren. |
| `pip install` scheitert (Timeout, SSL, 407) | Firmenproxy: vorher `$env:HTTPS_PROXY = "http://proxy:port"` setzen und den Befehl wiederholen. Interner PyPI-Spiegel: `.venv\Scripts\python.exe -m pip config set global.index-url <URL>`. |
| `Address already in use` / Port 8000 belegt | `--port 8080` an den Startbefehl anhängen und in den Übungen `8080` statt `8000` verwenden. |
| `Invoke-WebRequest` meldet einen Proxy-Fehler | Firmenproxy leitet auch `127.0.0.1` um. Prüfung im Browser genügt. |
| Seite lädt nicht | Läuft die App noch im ersten Fenster? Fehlermeldung dort lesen. Adresse genau `http://127.0.0.1:8000` (nicht https). |
| Tests rot | Ausgabe lesen. Meist unvollständige Installation → Schritt 4 wiederholen. |
| VS Code findet den Interpreter nicht | Schritt 8. Falls `.venv` nicht angeboten wird: „Enter interpreter path“ → `.venv\Scripts\python.exe`. |

macOS/Linux: `python3 -m venv .venv` und `.venv/bin/python` statt `.venv\Scripts\python.exe`.
