# ADR-002: Migrationen als nummerierte SQL-Dateien

Status: akzeptiert · Datum: 2026-06-02

## Kontext

Wir brauchen reproduzierbare Schemaänderungen, wollen aber kein Migrationsframework einführen (siehe ADR-001).

## Entscheidung

Migrationen liegen als `NNN_kurzname.sql` in `app/migrations/`. Beim Anwendungsstart werden noch nicht angewendete Dateien der Reihe nach ausgeführt, jede in einer eigenen Transaktion, und in der Tabelle `schema_migrations` protokolliert. Committete Dateien werden nie geändert, denn eine bereits angewendete Migration wird nicht erneut ausgeführt; jede Schemaänderung ist eine neue Datei.

## Konsequenzen

- Einfach zu lesen und zu reviewen.
- Keine Down-Migrationen; Rückbau ist eine neue Vorwärts-Migration.
- Nachtrag 2026-09-23: Anfangs liefen bei jedem Start alle Migrationen erneut und mussten idempotent sein. Das scheiterte an `ALTER TABLE … ADD COLUMN`, das sich in SQLite nicht idempotent formulieren lässt. Seitdem protokolliert `schema_migrations` die angewendeten Dateien.
- Seed-Daten sind ebenfalls eine Migration (`002_seed.sql`), damit jede Umgebung dieselben Demodaten hat.
