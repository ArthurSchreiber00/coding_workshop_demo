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
    """Führt alle app/migrations/NNN_*.sql in Reihenfolge aus. Dateien müssen idempotent sein."""
    applied: list[str] = []
    conn = connect()
    try:
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            conn.executescript(path.read_text(encoding="utf-8"))
            applied.append(path.name)
        conn.commit()
    finally:
        conn.close()
    return applied


def get_conn() -> Iterator[sqlite3.Connection]:
    """FastAPI-Dependency: eine Verbindung pro Request, Commit am Ende."""
    conn = connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
