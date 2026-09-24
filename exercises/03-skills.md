# 3 · Skills (35 min)

**Ziel:** Zwei Skills bauen, die Copilot automatisch lädt, wenn sie passen.

## A · `toolshed-api` – Wissen plus Skript (20 min)

1. Agent-Modus: `/create-skill` eingeben und den Skill `toolshed-api` selbst beschreiben. Er soll Copilot beibringen, mit der laufenden API zu arbeiten, und ein Python-Skript mitbringen, das die wichtigsten Aktionen ausführt. Nützliche Fakten: Basis-URL `http://127.0.0.1:8000`, Header `X-Api-Key` aus `app/config.py`, Endpunkte unter `/openapi.json`, nur `httpx` aus `requirements.txt` verwenden.
2. Ergebnis in `.github/skills/toolshed-api/` prüfen: `name` = Ordnername. Nennt die `description` die Situationen, in denen der Skill greifen soll? Das Skript einmal im Terminal ausprobieren.
3. Neuer Chat, Agent: eine Frage stellen, zu der der Skill passt, ohne ihn zu nennen. Erwartet: Copilot liest die `SKILL.md` und führt das Skript aus.
4. Den Skill explizit aufrufen: `/toolshed-api` und dahinter ein eigener Auftrag, z. B. eine Ausleihe anlegen.

## B · `add-resource` – nur Wissen (15 min)

1. Mit `/create-skill` den Skill `add-resource` selbst beschreiben: wie in diesem Repo eine neue Entität end-to-end entsteht, von der Migration bis zu den Tests, nach `docs/conventions.md` und `docs/architecture.md`.
2. Im Plan-Modus testen: eine neue Entität anfragen, z. B. Standorte, denen Geräte zugeordnet sind. Erwartet: Agent nutzt den Skill, Plan folgt der Reihenfolge aus dem Skill, neue Migration mit der nächsten freien Nummer.

**Merke:** Nur `name` und `description` sind immer im Kontext, der Rest wird bei Bedarf geladen. Die `description` entscheidet über das Laden. Skills ersetzen Prompt-Files.

**Wenn es klemmt**
- Skill wird nicht geladen → `description` konkreter, Ordnername = `name`, Chat neu starten. Copilot fragen, welche Skills er kennt.
- Skript fragt nach Bestätigung → im Chat bestätigen (Terminal-Tool).
