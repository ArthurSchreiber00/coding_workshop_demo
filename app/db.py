"""SQLite-Verbindung und Migrationen."""
import os
import sqlite3
from collections.abc import Iterator
from pathlib import Path

from app import config

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def get_db_path() -> str:
    return os.environ.get("TOOLSHED_DB") or config.DB_PATH


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def run_migrations() -> list[str]:
    """Wendet neue app/migrations/NNN_*.sql in Reihenfolge an, jede genau einmal.

    Bereits angewendete Dateien stehen in der Tabelle schema_migrations. Jede Migration
    läuft zusammen mit ihrem Protokolleintrag in einer Transaktion: Schlägt sie fehl,
    bleibt die Datenbank unverändert und die Migration gilt als nicht angewendet.
    Gibt die Namen der in diesem Aufruf neu angewendeten Migrationen zurück.
    """
    newly_applied: list[str] = []
    conn = connect()
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            " name TEXT PRIMARY KEY,"
            " applied_at TEXT NOT NULL DEFAULT (datetime('now')))"
        )
        conn.commit()
        done = {row["name"] for row in conn.execute("SELECT name FROM schema_migrations")}
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if path.name in done:
                continue
            try:
                # executescript committet vorher offene Transaktionen und steuert selbst keine;
                # das BEGIN hält Migration und Protokolleintrag in einer Transaktion.
                conn.executescript("BEGIN;\n" + path.read_text(encoding="utf-8"))
                conn.execute("INSERT INTO schema_migrations (name) VALUES (?)", (path.name,))
                conn.commit()
            except sqlite3.Error as exc:
                conn.rollback()
                raise RuntimeError(f"Migration {path.name} fehlgeschlagen: {exc}") from exc
            newly_applied.append(path.name)
    finally:
        conn.close()
    return newly_applied


def get_conn() -> Iterator[sqlite3.Connection]:
    """FastAPI-Dependency: eine Verbindung pro Request, Commit am Ende."""
    conn = connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
