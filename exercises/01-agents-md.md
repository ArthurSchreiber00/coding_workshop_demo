# 1 · AGENTS.md (25 min)

**Ziel:** Copilot kennt die Regeln dieses Repos, ohne dass wir sie in jedem Prompt wiederholen.

1. Leere Datei `AGENTS.md` im Projektstamm anlegen. (Sonst schreibt `/init` nach `.github/copilot-instructions.md`.)
2. Copilot Chat, Modus **Agent**, eingeben:
   ```
   /init
   ```
3. Ergebnis lesen und mit `docs/conventions.md` abgleichen. Was fehlt oder ist zu allgemein? Typisch: Migrationen nie ändern, Fehlerformat, `X-Api-Key`, Testkommando, kein ORM.
4. Datei überarbeiten. Struktur: **Kommandos** · **Stack** · **Struktur** · **Stil** (ein echtes Beispiel) · **Grenzen** (immer / erst fragen / nie). Höchstens eine Seite. Auf `docs/` verlinken statt kopieren.
5. Prüfen – neuer Chat, Frage:
   ```
   Wie lege ich in diesem Projekt eine Schemaänderung an?
   ```
   Erwartet: Antwort nennt eine neue Migrationsdatei mit nächster Nummer. Oben in der Antwort **References** aufklappen → `AGENTS.md` ist gelistet.

**Bonus:** `/create-instructions` für eine Regel, die nur für `app/templates/**` gilt (z. B. „jedes Formularfeld hat ein `<label>`“).

**Wenn es klemmt**
- `/init` hat `.github/copilot-instructions.md` erzeugt → Inhalt nach `AGENTS.md` verschieben, Datei löschen.
- `AGENTS.md` fehlt in References → Chat-Ansicht Rechtsklick → **Diagnostics** zeigt geladene Instruktionsdateien.
