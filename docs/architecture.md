# Architektur

Toolshed ist eine kleine Web-App zur Verwaltung von Geräteausleihen im Team.

## Schichten

```
Browser / API-Client
        │
        ▼
app/routers/        HTTP-Schicht: Request lesen, validieren, Antwort bauen.
  pages.py          HTML-Seiten (Jinja2)
  items.py …        JSON-API unter /api
        │
        ▼
app/repositories/   Datenzugriff: ausschließlich hier steht SQL.
        │
        ▼
app/db.py           SQLite-Verbindung, Migrationen beim Start.
```

Regeln:

- **Router sind dünn.** Kein SQL in Routern, keine Geschäftsregeln in Templates.
- **Repositories enthalten nur SQL** und geben einfache `dict`s bzw. Pydantic-Modelle zurück.
- **Geschäftsregeln** (z. B. „maximal 3 offene Ausleihen pro Person“) gehören in eine eigene Funktion, die von *allen* Einstiegspunkten (HTML-Formular und JSON-API) benutzt wird.
- **Konfiguration** kommt aus `app/config.py`, nirgendwo sonst aus `os.environ`.

## Datenmodell

`items` (Geräte) — `members` (Personen) — `loans` (Ausleihen). Eine Ausleihe ist offen, solange `returned_at` NULL ist.
Datumsfelder sind ISO-Strings (`YYYY-MM-DD`).

## Warum kein ORM?

Siehe [ADR-001](decisions/ADR-001-raw-sql.md). Kurz: die App ist klein, SQL bleibt sichtbar und lehrbar, keine zusätzliche Abhängigkeit.

## Bekannte Abweichungen

Die Codebasis ist absichtlich nicht perfekt. Ein Teil der Workshop-Übungen besteht darin, Abweichungen von dieser Architektur zu finden.
