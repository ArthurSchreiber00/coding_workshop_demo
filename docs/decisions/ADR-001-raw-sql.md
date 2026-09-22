# ADR-001: SQLite mit rohem SQL statt ORM

Status: akzeptiert · Datum: 2026-06-02

## Kontext

Toolshed ist ein kleines internes Werkzeug mit drei Tabellen. Das Team wollte eine Codebasis, in der man das Datenmodell direkt sieht und die ohne zusätzliche Bibliotheken auskommt.

## Entscheidung

Wir benutzen `sqlite3` aus der Standardbibliothek. SQL steht ausschließlich in `app/repositories/`, immer mit Parameter-Platzhaltern.

## Konsequenzen

- Keine Abhängigkeit von einem ORM, kein Mapping-Overhead.
- Mehr Disziplin nötig: Abfragen müssen von Hand geschrieben und getestet werden.
- Ein Wechsel auf PostgreSQL wäre Handarbeit; für den aktuellen Umfang akzeptabel.
