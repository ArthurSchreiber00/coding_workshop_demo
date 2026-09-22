# 3 · Skills (35 min)

**Ziel:** Zwei Skills bauen, die Copilot automatisch lädt, wenn sie passen.

## A · `toolshed-api` – Wissen plus Skript (20 min)

1. Agent-Modus:
   ```
   /create-skill Skill "toolshed-api": wie man mit der laufenden Toolshed-API arbeitet (Basis-URL http://127.0.0.1:8000, Header X-Api-Key aus app/config.py, Endpunkte laut /openapi.json, Fehlerformat). Enthält ein Python-Skript scripts/api.py mit Unterbefehlen: items, members, loans, overdue, lend, return. Nur httpx aus requirements.txt verwenden.
   ```
2. Ergebnis prüfen: `.github/skills/toolshed-api/SKILL.md`. `name` = Ordnername. `description` nennt Auslöser wie „API aufrufen“, „Ausleihe anlegen“, „überfällige Ausleihen“, „Demodaten“. Skript testen:
   ```powershell
   .venv\Scripts\python.exe .github\skills\toolshed-api\scripts\api.py overdue
   ```
3. Auslösen lassen – neuer Chat, Agent:
   ```
   Welche Ausleihen sind überfällig? Nutze die laufende API.
   ```
   Erwartet: References zeigt den Skill, das Skript wird ausgeführt.
4. Explizit aufrufen:
   ```
   /toolshed-api Leih die Sony A7 IV an Mira Schulz aus, Rückgabe in einer Woche.
   ```

## B · `add-resource` – nur Wissen (15 min)

1. ```
   /create-skill Skill "add-resource": wie in diesem Repo eine neue Entität end-to-end angelegt wird – Migration, Repository, Schema, Router, Template, Tests – nach docs/conventions.md und docs/architecture.md.
   ```
2. Testen (Plan-Modus reicht):
   ```
   Füge eine Entität "Location" hinzu, der Geräte zugeordnet sind.
   ```
   Erwartet: Plan folgt der Reihenfolge aus dem Skill, neue Migration `003_…`.

**Merke:** Nur `name` und `description` sind immer im Kontext, der Rest wird bei Bedarf geladen. Die `description` entscheidet über das Laden. Skills ersetzen Prompt-Files.

**Wenn es klemmt**
- Skill wird nicht geladen → `description` konkreter, Ordnername = `name`, Chat neu starten. „Welche Skills hast du?“ zeigt die geladenen.
- Skript fragt nach Bestätigung → im Chat bestätigen (Terminal-Tool).
