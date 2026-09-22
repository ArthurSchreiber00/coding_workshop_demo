-- 001: Grundschema. Committete Migrationen werden nie geändert (siehe docs/conventions.md).
CREATE TABLE IF NOT EXISTS items (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    category      TEXT    NOT NULL,
    inventory_no  TEXT    NOT NULL UNIQUE,
    status        TEXT    NOT NULL DEFAULT 'available'
                          CHECK (status IN ('available', 'on_loan', 'maintenance')),
    notes         TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS members (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    team       TEXT NOT NULL,
    is_admin   INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS loans (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id     INTEGER NOT NULL REFERENCES items(id),
    member_id   INTEGER NOT NULL REFERENCES members(id),
    loaned_at   TEXT    NOT NULL,   -- ISO-Datum YYYY-MM-DD
    due_date    TEXT    NOT NULL,   -- ISO-Datum YYYY-MM-DD
    returned_at TEXT,               -- NULL = noch ausgeliehen
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_loans_item   ON loans(item_id);
CREATE INDEX IF NOT EXISTS idx_loans_member ON loans(member_id);
