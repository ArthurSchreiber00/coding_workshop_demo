# 5 · Review aus drei Perspektiven mit Custom Agents (45 min)

**Ziel:** Ein Orchestrator-Agent lässt drei spezialisierte Reviewer parallel als Subagenten laufen und fasst ihre Ergebnisse zusammen.

**Vorbereitung:** `git checkout feature/quick-fixes` – der Branch enthält absichtlich fehlerhafte Änderungen. Alternativ die eigenen Änderungen aus Übung 2/3 reviewen.

## 1 · Drei Reviewer (15 min)

Dateien in `.github/agents/`: `security-reviewer.agent.md`, `accessibility-reviewer.agent.md`, `architecture-reviewer.agent.md` (per `/create-agent` oder von Hand). Frontmatter jeweils:

```yaml
---
name: security-reviewer
description: Prüft einen Diff ausschließlich auf Sicherheitsprobleme. Nur als Subagent verwenden.
user-invocable: false
tools: ['read', 'search', 'search/changes']
---
```

Body: nur diese Perspektive · Eingabe ist ein Diff · Ausgabe als Tabelle **Schwere · Datei:Zeile · Problem · Vorschlag** · keine Codeänderungen.

Checklisten:
- **Security:** Injection, fehlende Autorisierung, Secrets im Code, Path Traversal, zu ausführliche Fehlermeldungen.
- **Accessibility (WCAG 2.2 AA):** Labels, Alt-Texte, Kontrast, Tastaturbedienung, Fokus sichtbar, Tabellenköpfe, Sprache.
- **Architecture:** gegen `docs/architecture.md` – dünne Router, SQL nur in Repositories, Geschäftsregeln zentral, Konfiguration zentral, keine Duplikate.

## 2 · Orchestrator (10 min)

`.github/agents/review-orchestrator.agent.md`:

```yaml
---
name: review-orchestrator
description: Review aus den Perspektiven Security, Accessibility und Architektur; startet die Reviewer parallel und aggregiert.
tools: ['agent', 'read', 'search', 'search/changes', 'execute']
agents: ['security-reviewer', 'accessibility-reviewer', 'architecture-reviewer']
---
```

Body: Diff holen (`#changes` oder `git diff main...HEAD`) → die drei Reviewer **parallel** als Subagenten starten und den vollständigen Diff mitgeben → nicht selbst reviewen → Ergebnisse zusammenführen: Duplikate entfernen, nach Schwere sortieren, Perspektive kennzeichnen, Gesamturteil (Blocker / vor Merge beheben / OK) → nach `docs/reviews/<datum>.md` schreiben → keine Codeänderungen.

## 3 · Ausführen (15 min)

Dropdown → **review-orchestrator**:
```
Reviewe die Änderungen dieses Branches gegenüber main.
```
Subagenten im Chat beobachten (aufklappbar). Bericht lesen. Was wurde gefunden, was übersehen?

## Bonus (5 min)

`.github/skills/multi-review/SKILL.md`, damit `/multi-review` im normalen Agent-Modus funktioniert. Die Anweisungen starten die drei Reviewer direkt – nicht den Orchestrator, denn verschachtelte Subagenten sind standardmäßig aus.

**Merke:** Agent = Rolle + eingeschränkte Tools + eigenes Modell + isolierter Kontext. Skill = Wissen und Ablauf. Höchstens vier Subagenten gleichzeitig.

**Wenn es klemmt**
- Agent fehlt im Dropdown → Dateiname endet auf `.agent.md`, YAML gültig, Chat neu laden.
- Subagenten laufen nicht → Reviewer einzeln im Dropdown starten (`user-invocable` vorübergehend entfernen) und die drei Berichte vom Agent zusammenfassen lassen.
