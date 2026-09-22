# ADR-002: Migrationen als nummerierte SQL-Dateien

Status: akzeptiert · Datum: 2026-06-02

## Kontext

Wir brauchen reproduzierbare Schemaänderungen, wollen aber kein Migrationsframework einführen (siehe ADR-001).

## Entscheidung

Migrationen liegen als `NNN_kurzname.sql` in `app/migrations/` und werden beim Anwendungsstart der Reihe nach ausgeführt. Jede Datei muss idempotent sein. Committete Dateien werden nie geändert; jede Schemaänderung ist eine neue Datei.

## Konsequenzen

- Einfach zu lesen und zu reviewen.
- Keine Down-Migrationen; Rückbau ist eine neue Vorwärts-Migration.
- Seed-Daten sind ebenfalls eine Migration (`002_seed.sql`), damit jede Umgebung dieselben Demodaten hat.
