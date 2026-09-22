# Workshop plan: AI-assisted coding with GitHub Copilot — demo repo & exercises

Status: research complete, all decisions taken with Arthur (section 7), nothing built yet. Date: 2026-09-22.
Target audience: developers at a large company, managed **Windows** laptops, GitHub Copilot **Enterprise**, **VS Code only**. Facilitator works on macOS. Participants know some Python.
Facilitator creates the slides; this repo provides the hands-on part.

---

## 0. Recommendations at a glance

| Topic | Recommendation | Why (short) |
|---|---|---|
| Demo app | **Toolshed** — a small equipment-lending web app: FastAPI + Jinja2 templates + SQLite, pytest. Pip-only dependencies, no Node/Docker. | Has an HTML UI (accessibility review), a REST API (skills + MCP), a data layer (security review), and layers to violate (architecture review). Small enough to understand in 10 minutes. |
| Module order | Setup → **AGENTS.md** → Plan mode → Skills → MCP → Custom agents & multi-perspective review | AGENTS.md first (Arthur's decision): every later exercise then runs with the conventions in place. Skills before agents because the review module builds on both. |
| AGENTS.md | Built-in `/init`, then refine by hand along the recommended structure (commands, stack, structure, style examples, boundaries) and verify via the References list. | Official generator. Gotcha: it writes `.github/copilot-instructions.md` unless an `AGENTS.md` already exists → create an empty `AGENTS.md` first. |
| Skills | Participants build two: `toolshed-api` (with a bundled Python script + OpenAPI reference) and `add-resource` (pure conventions). Use `/create-skill`. | Covers both skill styles: bundled scripts and encoded team conventions. Prompt files are deprecated in favour of skills, so skills are the thing to teach. |
| Custom agents | Still relevant, and exactly right for the review use case. | Only agents can restrict tools, pin a model, run as isolated parallel subagents, and declare which subagents they may call. Skills cannot do any of that. |
| Multi-perspective review | **3 read-only reviewer agents + 1 orchestrator agent** (`tools: ['agent', …]`, `agents: […]`), optional thin `/multi-review` skill as launcher. Not a single skill. | Documented, GA, parallel, isolated contexts. Pattern is endorsed in GitHub's own learning hub ("Multi-Perspective Review"). |
| MCP | Zero-install: remote HTTP servers without auth (Microsoft Learn, DeepWiki, Context7) for a warm-up, then the repo's own **Python MCP server** (official `mcp` SDK, streamable HTTP on localhost). | No npx/docker needed. Biggest risk is not technical: the org policy "MCP servers in Copilot" is **off by default** for Business/Enterprise. |
| Copilot CLI | Not part of the plan. | Needs npm/winget/brew install; unlikely on managed devices. Everything is designed for VS Code. |

All decisions: see **section 7**.

---

## 1. Research findings that shape the design

Everything below is from official docs (VS Code, GitHub Docs, GitHub Changelog), GitHub's own workshop material (copilot-academy.github.io, github/awesome-copilot), or the public source of the Copilot Chat extension. Where something is inference or unverified, it says so.

### 1.1 Plan mode (VS Code)

- Official name: the built-in **Plan** agent. Selected in the agents dropdown of the Chat view, or started with `/plan <task>`. Stable since VS Code 1.106 (Oct 2025); on by default, no setting needed. Available on all Copilot plans.
- Workflow baked into its prompt: Discovery (read-only exploration, may spawn an Explore subagent) → Alignment (asks clarifying questions, often with options) → Design → Refinement. It never edits files.
- Output is a Markdown plan in chat with a fixed structure (TL;DR, Steps, Relevant files, Verification, Decisions, Further considerations; explicitly no code blocks). It is auto-saved to the session memory file `/memories/session/plan.md`, not into the repo.
- Hand-off buttons after the plan: **Start Implementation** (switches to the implementation agent, plan context carries over) and **Open in Editor** (untitled `plan-*.prompt.md` for editing).
- Settings: `chat.planAgent.defaultModel`, `github.copilot.chat.implementAgent.model` (experimental), `github.copilot.chat.planAgent.additionalTools` (experimental; can give the planner MCP tools).
- Prompting tips from the docs: give a goal, not micro-steps; answer the clarifying questions; expect a few refinement rounds; point at an issue or spec file when one exists.
- You can open the built-in Plan agent's definition (gear icon → Agents → Plan) — a good slide/demo moment, and the basis for a custom planning agent with handoffs.

### 1.2 AGENTS.md and custom instructions

- Supported files in VS Code chat: root `AGENTS.md` (`chat.useAgentsMdFile`, on), `.github/copilot-instructions.md` (on), `CLAUDE.md` (on), `.github/instructions/*.instructions.md` with `applyTo` globs (on). Nested `AGENTS.md` in subfolders is experimental and off by default in VS Code (the cloud coding agent supports nesting with nearest-file-wins).
- Instructions apply to chat/agent requests only, never to inline completions. They are appended to every request, so size costs tokens every turn.
- **Generating one**: type `/init` in Copilot Chat (Agent mode). It discovers existing instruction files, explores the codebase with parallel subagents (build/test commands, architecture, non-obvious conventions), and creates `.github/copilot-instructions.md`, or updates `AGENTS.md` **only if one already exists**. Other entry points: `/create-instructions` (targeted `.instructions.md` with `applyTo`), the **Generate Instructions** entry in the Agent Customizations editor (gear icon). The old "Chat: Generate Workspace Instructions File" command is gone.
- Official guidance on content: executable commands early, tech stack with versions, project structure, real code-style examples, boundaries in three tiers (always / ask first / never), keep it short, link to docs instead of embedding, focus on non-obvious conventions, do not duplicate what linters enforce. (GitHub blog "How to write a great agents.md", analysis of 2,500+ repos.)
- Verifying it was used: expand the **References** list at the top of a chat response; the instruction file is listed there. Chat view context menu → **Diagnostics** shows all loaded instruction files.

### 1.3 Agent Skills

- Format: `.github/skills/<name>/SKILL.md` with YAML frontmatter `name` (must equal the folder name, lowercase-hyphen, otherwise the skill is not loaded) and `description` (the *only* thing Copilot uses to decide whether to load the skill — put trigger phrases there). Optional `argument-hint`, `user-invocable`, `disable-model-invocation`. Optional subfolders `scripts/`, `references/`, `assets/` referenced by relative Markdown links.
- Progressive disclosure: only name + description are always in context; the body loads when matched; referenced files load on demand; scripts run via the terminal tool without being loaded.
- GA in VS Code since 1.109 (Jan 2026), also in Copilot CLI, cloud coding agent, Copilot code review (GA July 2026). Setting `chat.useAgentSkills` (default true).
- Invocation: automatic by description match, or explicitly `/skill-name optional context`.
- Creating: built-in `/create-skill` (asks clarifying questions, writes the SKILL.md), Command Palette **Chat: New Skill File**, or the Agent Customizations editor. Anthropic's `skill-creator` meta-skill can also be copied into `.github/skills/` (no install, just files). `gh skill install github/awesome-copilot <skill>` exists but needs GitHub CLI ≥ 2.90 — do not rely on it.
- Scripts inside skills: yes, any language the machine can run; executed through the terminal tool with the normal confirmation. A Python script fits this audience.
- Prompt files (`.prompt.md`) are **deprecated** for the new Agent Host sessions and VS Code migrates them to skills. Teach skills, mention prompt files only historically.
- Official decision guidance (GitHub Docs): always-on conventions → custom instructions; repeatable on-demand workflow → skill; specialist with a constrained toolset → custom agent; external tools → MCP; guardrails/automation around tool use → hooks.

### 1.4 Custom agents and subagents

- Format: `.github/agents/<name>.agent.md`. Frontmatter: `name`, `description` (required), `tools` (omit = all tools; list restricts), `model` (string or fallback array), `agents` (allowlist of subagents this agent may invoke; `*` = all; `[]` = none), `user-invocable` (false = hidden from dropdown, usable only as subagent), `disable-model-invocation` (true = never auto-selected as subagent), `handoffs` (buttons that switch to another agent with a pre-filled prompt; `send: true` auto-submits), `argument-hint`, `hooks` (preview). The old `infer` flag is deprecated. Body = system prompt, max 30,000 chars.
- Subagents: the main agent (or a custom agent that has the `agent` tool) delegates a subtask to another agent, which runs in an **isolated context window** and returns only a summary. Subagents **run in parallel** (VS Code 1.109+). Stateless: no follow-up messages, so the task must contain all context. Nesting (subagent spawning subagents) is **off by default** (`chat.subagents.allowInvocationsFromSubagents`). An open VS Code issue reports a hard cap of **4 concurrent subagents** — three reviewers fit.
- Created via `/create-agent`, **Chat: New Custom Agent**, or the gear icon → Agents.
- When custom agents are the right choice (vs. skills): you need a **persona with restricted tools** (read-only reviewer or planner), a **different model per role**, **context isolation / parallelism** via subagents, an **orchestrator** that declares which sub-agents it may call, or handoff chains. Skills are the right choice for reusable procedures and bundled scripts that any agent should be able to pick up. GitHub's own decision matrix: "You only need guidance text → a skill is the lighter-weight solution."
- Harness caveat: VS Code now has a "Local" harness and a "Copilot" harness (Agent Host, powered by the Copilot SDK) which is becoming the default. Custom agents, skills and hooks work on both; prompt files do not. Whether the `agents:` allowlist and the parallel cap behave identically in both harnesses is not explicitly documented → **smoke-test on the exact VS Code version the participants will have**.

### 1.5 MCP

- Config: `.vscode/mcp.json` with top-level `servers` (note: Copilot CLI and Claude use `mcpServers`; wrong key = server silently absent). Types: `stdio` (`command`, `args`, `cwd`, `env`) and `http` (`url`, `headers`). Servers using `${input:…}` prompts are **not** forwarded to the Agent Host harness, so avoid inputs; none of the proposed servers need secrets.
- Managing: code lenses in `mcp.json` (Start/Stop/Restart), **MCP: List Servers**, **Show Output** for server stderr, **MCP: Reset Cached Tools** after changing tool signatures. Tools appear in the tools picker grouped per server; reference with `#servername/tool`. Hard limit of 128 enabled tools per request.
- Remote servers that need **no local runtime and no auth**: Microsoft Learn (`https://learn.microsoft.com/api/mcp`), DeepWiki (`https://mcp.deepwiki.com/mcp`), Context7 (`https://mcp.context7.com/mcp`, anonymous with rate limit). GitHub's remote MCP server (`https://api.githubcopilot.com/mcp/`) uses browser OAuth — nice, but depends on the org policy and GitHub access from the laptop.
- Own server in Python: official `mcp` package on PyPI, **v2.x** (Sept 2026; Python ≥ 3.10). API: `from mcp.server import MCPServer`, `@mcp.tool()`, `mcp.run(transport="streamable-http", port=8001)` → `http://127.0.0.1:8001/mcp`. **Breaking change vs. most tutorials**: v1 was `from mcp.server.fastmcp import FastMCP`; pin the version in `requirements.txt`. It can also be mounted into the FastAPI app (needs the MCP session manager in the app lifespan). The `mcp dev` inspector needs Node — not usable; test with the SDK's Python `Client` instead.
- **Policies** (the real risk): GitHub org/enterprise policy **"MCP servers in Copilot"** is disabled by default and governs Business/Enterprise seats; there may also be "Restrict MCP access to registry servers" (would block a localhost server) and VS Code device policies (`ChatMCP`, `ChatAllowedMcpServers`). Participants can check with **Developer: Policy Diagnostics**. Must be confirmed with the customer's admin beforehand.
- Windows gotchas for stdio servers: use `python` or the absolute venv interpreter (`${workspaceFolder}/.venv/Scripts/python.exe`), never `python3`; never `print()` to stdout in a stdio server. The streamable-HTTP design avoids all of this: participants just run the server in a terminal and VS Code connects by URL.

### 1.6 Multi-perspective review — which primitive?

| Option | Verdict |
|---|---|
| One skill with a three-part checklist | Simplest and portable (also read by github.com code review), but one context and one model: the perspectives anchor on each other, and a long checklist competes with the diff for context. Good as a *fallback*, not as the main design. |
| A skill that instructs the agent to launch three reviewer agents as subagents and aggregate | Works if the currently selected agent has the `agent` tool (the default Agent does). Reliability depends on the model following the text; a skill has no `tools:`/`agents:` frontmatter in the docs. Good as the **`/multi-review` launcher** on top of option C. Caveat: the skill must fan out to the three reviewers directly, not to the orchestrator agent, because nesting is off by default. |
| **3 reviewer agents + 1 orchestrator agent (subagents)** | **Recommended.** Fully documented: `tools: ['agent', …]`, `agents: [...]`, `user-invocable: false` on workers, parallel isolated runs, per-perspective read-only tools and optional per-perspective model, documented return path. Exactly GitHub's "Multi-Perspective Review" pattern. |
| Handoffs | Sequential user-clicked buttons; not aggregation. Show on a slide, don't build on it. |
| Prompt file with `agent:` | Deprecated on Agent Host. Skip. |
| Copilot code review on github.com | The CI counterpart: reads `AGENTS.md`, `.github/instructions/*.instructions.md` (with `excludeAgent`), skills and MCP from the PR head branch. Single persona, no isolated perspectives, no custom agents. Optional module if the repo lives in their GitHub org. |
| Hooks | Deterministic triggers (Stop / PostToolUse) but run shell commands, not agents. Optional bonus. |

Getting the diff into the review: chat variable `#changes` (tool id `search/changes`), or `git diff` / `git diff --staged` / `git diff main...HEAD` via the terminal tool. For stateless subagents the orchestrator should paste the diff text into each task.

---

## 2. Demo app proposal: "Toolshed"

An equipment-lending tracker for a team: **items** (laptops, projectors, cameras…), **members**, **loans** (who has what, due when). Neutral domain, obvious feature ideas, obvious data model. Name is a placeholder.

### 2.1 Stack (all pip-installable)

| Package | Purpose |
|---|---|
| `fastapi`, `uvicorn` | API + server; OpenAPI docs at `/docs` for free (useful for the API skill and the MCP server) |
| `jinja2`, `python-multipart` | Server-rendered HTML pages and forms (accessibility review target) |
| `sqlite3` (stdlib) | Data layer with raw SQL and simple `.sql` migration files (security + architecture review targets; no extra dependency) |
| `pytest`, `httpx` | Tests via FastAPI's TestClient |
| `mcp` (pinned 2.x) | The repo's own MCP server |

Python 3.11+ recommended (3.10 minimum for `mcp`). Run: `python -m uvicorn app.main:app --reload`. Tests: `python -m pytest -q`. No Makefile (Windows), commands documented in README and later in AGENTS.md.

### 2.2 Layout

```
toolshed/
  README.md                    what it is, how to run, how to test (participant-facing)
  exercises/                   one Markdown sheet per module (01-plan-mode.md … 06-review.md)
  requirements.txt
  app/
    main.py                    FastAPI app, routers, templates, startup migration
    config.py                  settings — with a planted hard-coded secret
    db.py                      sqlite connection + migration runner (convention: app/migrations/NNN_name.sql)
    migrations/001_init.sql, 002_seed.sql
    routers/pages.py           HTML pages (Jinja2)
    routers/items.py, members.py, loans.py   JSON API under /api
    repositories/items.py, loans.py          data access — but some routes bypass it on purpose
    schemas.py                 pydantic models
    templates/base.html, index.html, items.html, item_form.html, loans.html
    static/styles.css, app.js  small; contains planted a11y issues
  tests/conftest.py, test_items.py, test_loans.py
  mcp_server/server.py         Python MCP server (streamable HTTP) wrapping the API
  docs/architecture.md         intended layering — the architecture reviewer reviews against this
  docs/conventions.md          naming, migrations, error format, testing conventions
  docs/decisions/ADR-001-*.md  one or two ADRs
  .vscode/mcp.json             remote no-auth servers + the local one (commented out until the MCP module)
  .vscode/settings.json, extensions.json
  .github/workflows/ci.yml     pytest on push (if hosted on GitHub)
  .github/                     agents/ and skills/ are created BY THE PARTICIPANTS; the repo ships without them
```

Facilitator material (solutions, reference AGENTS.md, reference agents/skills, planted-issue list) lives on a separate `solutions` branch or in a private facilitator repo so participants cannot peek.

### 2.3 Deliberately planted material

- **Non-obvious conventions** for `/init` and AGENTS.md to discover (some documented in `docs/`, some only visible in code): migrations are plain `.sql` files applied at startup and must never be edited after commit; API errors use one JSON shape `{"error": {"code", "message"}}`; tests need `TOOLSHED_DB=:memory:`; UI strings live in one place; raw SQL by choice (no ORM), always parameterised.
- **Security issues** (for the security reviewer): string-formatted SQL in the item search endpoint; admin endpoint to delete members without any auth check; hard-coded `SECRET_KEY` in `config.py`; file download endpoint with path traversal; verbose exception details returned to the client.
- **Accessibility issues**: form inputs without `<label>`, icon-only buttons without text, images without `alt`, low-contrast status badges, table without header scope, focus outline removed in CSS, a custom dropdown in `app.js` not keyboard-operable.
- **Architecture issues**: one router does SQL directly instead of using the repository; duplicated date-parsing logic in two routers; business rule (max 3 open loans per member) implemented in the template layer; config read in three different ways.
- A prepared branch `feature/quick-fixes` (or a patch file) with a small flawed change touching all three areas, so the review module has guaranteed findings even if a participant's own work is clean.

---

## 3. Workshop flow and exercise designs

Budget: full day, about half of it hands-on (≈ 3.5 h). Modules 0–5 below sum to ≈ 3h10, leaving ~20 min buffer. Timings exclude lecture time. All commands in the sheets are PowerShell.

### Module 0 — Setup (15 min)

- Clone the public repo, `py -3 -m venv .venv`, `.venv\Scripts\python.exe -m pip install -r requirements.txt` (no activation script → no PowerShell execution-policy issue), run server, open `http://127.0.0.1:8000`, run tests.
- Check Copilot: Agent mode works, models available, Plan appears in the agents dropdown.
- Facilitator checklist: VS Code version ≥ 1.109 recommended latest, Copilot Chat extension up to date.

### Module 1 — AGENTS.md (25 min)

- Repo state: ships **without** `AGENTS.md` or `copilot-instructions.md`; it does ship `README.md`, `docs/conventions.md`, `docs/architecture.md`, `CONTRIBUTING.md` for `/init` to find.
- Steps:
  1. Create an empty `AGENTS.md` (otherwise `/init` writes `.github/copilot-instructions.md`), run `/init` in Agent mode, read the result.
  2. Compare with the repo: what did it find (commands, stack, structure), what did it miss (the non-obvious conventions from 2.3, e.g. never edit committed migrations, error envelope, test env var, raw SQL by choice)?
  3. Refine along the recommended structure: commands first, stack with versions, structure, one or two real code-style examples, boundaries as always / ask first / never (never edit committed migrations, never commit secrets, ask before adding dependencies, no ORM). Link to `docs/conventions.md` instead of copying it. Keep it under one page.
  4. Verify: ask a convention question in a fresh chat and expand the **References** list → `AGENTS.md` is listed. Chat context menu → **Diagnostics** shows the loaded instruction files.
- Stretch: `/create-instructions` for a path-scoped rule (`app/templates/**` → accessibility rules). Discussion point: AGENTS.md is loaded on every request (token cost), path-scoped instructions only when matching files are touched, skills only on demand.

### Module 2 — Plan mode (30 min)

- Runs with the AGENTS.md from module 1 in place, so the plan respects the conventions.
- Feature (decision: the one that costs least time): **Overdue loans** — an overdue page with a badge count in the navigation, `GET /api/loans/overdue`, a "mark as returned" action, tests. Ambiguous enough for clarifying questions (grace period? sort order? what counts as overdue at midnight? who may mark returned?).
  - Reservations (date ranges, conflict rules) stays in the solutions repo as a stretch feature for fast participants.
- Steps: switch to **Plan**, prompt with a goal-level description (the sheet gives a deliberately vague PM-style request and a better version to compare), answer the clarifying questions, read the plan critically (steps, files, verification, decisions), refine once ("also add tests", "keep the route thin"), check that it follows AGENTS.md (new migration instead of editing one, error envelope, test command), then **Start Implementation**. Run tests + app. Time-box implementation; the learning goal is reading and steering the plan.
- Facilitator note: show the built-in Plan agent's definition (gear → Agents → Plan) and the **Open in Editor** button for keeping a plan as a file.

### Module 3 — Skills (35 min)

- Skill A `toolshed-api` (bundled script): when the user wants to call, seed, inspect or smoke-test the running API. Contains `scripts/api.py` (small httpx CLI: list items, seed demo data, list overdue loans, create loan) and `references/openapi.md` (trimmed OpenAPI summary + error format). Trigger test: "Seed five demo items and show me the overdue loans" → Copilot loads the skill and runs the script instead of guessing curl commands.
- Skill B `add-resource` (pure conventions): how to add a new entity end-to-end in this repo (migration → repository → schema → router → template → tests) following `docs/conventions.md`. Trigger test: "Add a `Location` entity that items belong to."
- Steps: use `/create-skill`, inspect the generated frontmatter, fix the description so it triggers reliably, test with a prompt that should trigger it and one that should not, then invoke explicitly with `/toolshed-api`.
- Teaching points: description is everything; folder name = `name`; progressive disclosure; skills vs instructions vs (deprecated) prompt files.

### Module 4 — MCP (30 min)

- Warm-up (5 min, zero install): `.vscode/mcp.json` already lists Microsoft Learn (and/or DeepWiki, Context7). Start it via code lens, open the tools picker, ask "How do I configure CORS in FastAPI? Use Microsoft Learn / Context7". Show `#servername/tool` references and the tool confirmation dialog.
- Main part: start the repo's MCP server `python mcp_server/server.py` (streamable HTTP on `127.0.0.1:8001/mcp`; tools: `list_items`, `search_items`, `list_overdue_loans`, `create_loan`, `return_item`; resource: `toolshed://schema`). Uncomment the `toolshed` entry in `mcp.json`, start, and drive the app from chat: "Which items are overdue and who has them? Create a loan of the projector for Dana until Friday." Show **Show Output** for server logs.
- Stretch: add a tool (`extend_loan`) to `server.py` with Copilot (Plan → implement), restart, **MCP: Reset Cached Tools**, try it.
- Teaching points: MCP = tools/resources/prompts over a protocol; http vs stdio; token cost of tool definitions and results; the skill from module 3 vs an MCP server for the same API (skill + script = cheaper and no server; MCP = live, typed, discoverable).
- Optional if policy and network allow: GitHub remote MCP server with OAuth (list issues of the repo).

### Module 5 — Custom agents & multi-perspective review (45 min)

- Prep: `git checkout feature/quick-fixes` (or apply patch) so there is a diff with known issues; or review the participant's own changes from modules 1–3.
- Step 1: create three worker agents with `/create-agent` or from a template in the exercise sheet: `security-reviewer`, `accessibility-reviewer`, `architecture-reviewer`. Each: `user-invocable: false`, read-only tools (`read`, `search`, `search/changes`), a fixed output format (severity, file:line, issue, fix), and a short checklist (OWASP Top 10 excerpt / WCAG 2.2 AA excerpt / `docs/architecture.md`). Optionally different `model` per reviewer to show the effect.
- Step 2: create `review-orchestrator`: `tools: ['agent', 'read', 'search', 'search/changes', 'execute']`, `agents: ['security-reviewer', 'accessibility-reviewer', 'architecture-reviewer']`; body: obtain the diff, run the three reviewers **in parallel** as subagents with the full diff in the task, do not review yourself, deduplicate, sort by severity, keep perspective tags, give an overall verdict, write `docs/reviews/<date>.md`, make no code changes.
- Step 3: select the orchestrator in the dropdown, run it, watch the subagents (collapsible tool calls / rich rendering), read the aggregated report, compare with the planted-issue list.
- Step 4 (optional launcher): `.github/skills/multi-review/SKILL.md` so `/multi-review` works from the default Agent; body contains the same fan-out instructions targeting the three reviewers directly (not the orchestrator — nesting is off by default).
- Teaching points: why agents here and not a skill (tool restriction, isolation, parallelism, model per role); statelessness of subagents; 4-concurrent cap; `disable-model-invocation` vs `user-invocable`; cost (three extra contexts).
- CI counterpart slide: `.github/instructions/review.instructions.md` with the same checklists is read by Copilot code review on github.com.

### Dropped by decision

Hooks, Copilot code review on github.com, GitHub remote MCP server, Copilot CLI. Hooks can be mentioned on one slide (deterministic guardrails/audit at agent lifecycle events; Preview) without an exercise.

---

## 4. What I will build (deliverables checklist)

1. The Toolshed app (code, seed data, tests, docs, ADRs), pip-only, verified on macOS by me and on Windows via the dry run in item 8. README in German.
2. Planted issues and conventions, plus a facilitator list of them with expected findings.
3. `mcp_server/server.py` (official `mcp` SDK 2.x, streamable HTTP), tested against VS Code, plus a tiny Python test client (no Node inspector).
4. `.vscode/mcp.json` (remote no-auth servers active, local server prepared), `settings.json`, `extensions.json`.
5. `exercises/00…06.md` — **German**, deliberately concise: one-line goal, numbered steps, copy-paste prompts, expected result, one "Wenn es klemmt" box, time box. No prose beyond that. Commands as PowerShell.
6. A separate **private** solutions repo (the public repo stays clean): reference `AGENTS.md`, a reference plan for Overdue loans from the dry run, `.github/skills/toolshed-api`, `.github/skills/add-resource`, `.github/agents/*.agent.md`, `.github/skills/multi-review`, reference implementation of Overdue loans, Reservations stretch feature, planted-issue list with expected findings. The `feature/quick-fixes` branch lives in the public repo because participants need it.
7. `PREREQUISITES.md` (German) → basis for your email to participants and their admin (section 5).
8. A smoke-test protocol for the exact VS Code/Copilot versions (both harnesses). **I develop on macOS and cannot run the Windows path myself**: the protocol needs one full run on a Windows machine (colleague, VM, or a participant-like laptop) before the workshop.
9. Public GitHub repo set up (name suggestion: `toolshed-copilot-workshop`), MIT licence, no solutions inside.

---

## 5. Prerequisites for the email (participants and their admin)

**Participants (installed and working before the workshop)**
- VS Code, latest stable (minimum 1.109), GitHub Copilot Chat extension up to date, signed in with their Copilot Business/Enterprise account; Agent mode available; check that **Plan** shows in the agents dropdown.
- Python 3.11+ (3.10 minimum) with `pip`, and permission to create a virtual environment and install these packages (exact pins will be in `requirements.txt`): `fastapi`, `uvicorn`, `jinja2`, `python-multipart`, `httpx`, `pytest`, `mcp`.
- Git for Windows (clone the public repo; the review module needs a real diff). PyPI is reachable (confirmed), so plain `pip install` works.
- Windows specifics baked into the sheets: `py -3 -m venv .venv` and `.venv\Scripts\python.exe -m …` everywhere, so no activation script and no execution-policy change is needed.
- Network access to `127.0.0.1` ports 8000/8001 from VS Code (local only), and outbound HTTPS to `learn.microsoft.com` (and optionally `mcp.deepwiki.com`, `mcp.context7.com`) for the MCP warm-up.

**Admin (Copilot policies)**
- Enterprise policy **"MCP servers in Copilot"** enabled (off by default). Check that "Restrict MCP access to registry servers" is not set to "Registry only" (that would block the local server). Check VS Code device policies `ChatMCP` / `ChatAllowedMcpServers`.
- Which models are enabled (Plan mode and the orchestrator work best with a strong model; reviewers can use a cheaper one).
- Optionally: Copilot CLI policy — not needed for this plan.

---

## 6. Risks and mitigations

| Risk | Mitigation |
|---|---|
| MCP policy disabled or localhost servers blocked | Confirm with admin two weeks ahead; fallback: MCP module becomes a facilitator demo + the API skill from module 3 covers the "talk to the API" use case. |
| Participants on different VS Code versions / harnesses | Pin a minimum version in the email; smoke-test both Local and Copilot harness; keep exercises to GA features (no prompt files, no hooks). |
| Facilitator on macOS, participants on Windows | Sheets written for PowerShell only; no venv activation; one complete Windows dry run before the workshop (colleague or VM). |
| Plan mode produces very different plans per participant | Fine for discussion; the solutions repo holds reference plans. |
| Subagent fan-out flaky in one harness | Fallback: run the three reviewers one after another via the dropdown, then ask the default agent to aggregate the three reports. |
| Time overrun | Each module has a stretch part that can be dropped; module 5 is the must-have finale. |

---

## 7. Decisions (2026-09-22)

Decided with Arthur:

| # | Topic | Decision | Consequence |
|---|---|---|---|
| 1 | OS | Participants Windows, facilitator macOS | PowerShell commands; Windows dry run required (section 4, item 8) |
| 2 | Copilot | Enterprise, VS Code only | Admin must confirm the MCP policy |
| 3 | Tooling | Git and PyPI reachable | Plain clone + `pip install` |
| 4 | Distribution | Public GitHub repo | Solutions go to a separate private repo |
| 5 | Language | Everything German, exercise sheets very concise | See deliverable 5 |
| 6 | Time | Full day, about half hands-on (~3.5 h) | Modules 0–5 sum to ~3h10, ~20 min buffer |
| 7 | Audience | Some Python knowledge | FastAPI stack confirmed |
| 9 | Plan-mode feature | Overdue loans (least time) | Reservations becomes a stretch feature |
| 10 | Optional modules | Hooks, Copilot code review on github.com and GitHub remote MCP dropped | Hooks get one slide at most, no exercise |
| 8 | Module order | **AGENTS.md first, then Plan mode** (Arthur's decision; the before/after comparison was judged too constructed) | Plan mode and all later modules run with conventions in place |
| 11 | Name | Toolshed | — |

No open decisions remain. Next step: build the repo (section 4).

---

## 8. Main sources

- VS Code docs: Plan agent (`/docs/copilot/agents/planning`), custom instructions (`/docs/agent-customization/custom-instructions`), agent skills (`/docs/agent-customization/agent-skills`), custom agents (`/docs/agent-customization/custom-agents`), subagents (`/docs/agents/run/subagents`), MCP servers (`/docs/agent-customization/mcp-servers`) and MCP configuration reference, hooks (`/docs/agent-customization/hooks`), agent harnesses (`/docs/agents/run/agent-harnesses`), release notes 1.106 / 1.109.
- GitHub Docs: custom agents configuration reference, customization cheat sheet, comparing CLI features (decision matrix), agent skills concepts, MCP policies (`manage-policies`, `configure-mcp-server-access`), custom instructions support matrix, hooks reference, Copilot code review customization.
- GitHub blog: "How to write a great agents.md", agent skills launch (2025-12-18), custom agents launch (2025-10-28), Copilot code review skills + MCP GA (2026-07-29), MCP GA in VS Code (2025-07-14).
- Copilot Academy (copilot-academy.github.io): Copilot Customization Handbook, Custom Agent Developer Guide, Agent Skills Developer Guide, "Customization in 90 Minutes" lab (code reviewer agent + orchestrator with `agents:`), Immersive Experience modules (planning, standards, skills, hooks); demo repo `copilot-academy/octocat_supply` (real `.github/agents`, `.github/skills`, `.github/hooks`, `.vscode/mcp.json`).
- awesome-copilot.github.com learning hub "Agents and Subagents" (Multi-Perspective Review pattern); github/awesome-copilot agents `se-security-reviewer`, `se-system-architecture-reviewer`, `accessibility`.
- MCP Python SDK (`py.sdk.modelcontextprotocol.io`: run, ASGI mounting, migration v1→v2), `modelcontextprotocol/python-sdk`, PyPI `mcp`.
- Open VS Code issues: #336440 (4 concurrent subagents cap), #332083 (Agent Host customization support).
