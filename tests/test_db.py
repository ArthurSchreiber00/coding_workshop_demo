"""Tests für den Migrations-Runner: jede Migration genau einmal, fehlgeschlagene gar nicht."""
import sqlite3

import pytest

from app import db


@pytest.fixture
def migrations(tmp_path, monkeypatch):
    """Eigenes Migrationsverzeichnis und eigene Datenbank pro Test."""
    mig_dir = tmp_path / "migrations"
    mig_dir.mkdir()
    monkeypatch.setattr(db, "MIGRATIONS_DIR", mig_dir)
    monkeypatch.setenv("TOOLSHED_DB", str(tmp_path / "migrations.db"))
    return mig_dir


def _columns(table: str) -> list[str]:
    conn = db.connect()
    try:
        return [row["name"] for row in conn.execute(f"PRAGMA table_info({table})")]
    finally:
        conn.close()


def test_real_migrations_apply_once(monkeypatch, tmp_path):
    monkeypatch.setenv("TOOLSHED_DB", str(tmp_path / "real.db"))
    first = db.run_migrations()
    assert first == sorted(p.name for p in db.MIGRATIONS_DIR.glob("*.sql"))
    assert db.run_migrations() == []


def test_add_column_migration_survives_restart(migrations):
    (migrations / "001_init.sql").write_text("CREATE TABLE items (id INTEGER PRIMARY KEY);", encoding="utf-8")
    (migrations / "002_add_location.sql").write_text("ALTER TABLE items ADD COLUMN location TEXT;", encoding="utf-8")

    assert db.run_migrations() == ["001_init.sql", "002_add_location.sql"]
    assert db.run_migrations() == []  # zweiter Start: nichts erneut ausführen
    assert _columns("items") == ["id", "location"]

    (migrations / "003_add_notes.sql").write_text("ALTER TABLE items ADD COLUMN notes TEXT;", encoding="utf-8")
    assert db.run_migrations() == ["003_add_notes.sql"]
    assert _columns("items") == ["id", "location", "notes"]


def test_failed_migration_is_rolled_back_and_not_recorded(migrations):
    (migrations / "001_init.sql").write_text("CREATE TABLE items (id INTEGER PRIMARY KEY);", encoding="utf-8")
    (migrations / "002_broken.sql").write_text(
        "CREATE TABLE locations (id INTEGER PRIMARY KEY);\nALTER TABLE does_not_exist ADD COLUMN x TEXT;",
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="002_broken.sql"):
        db.run_migrations()

    conn = db.connect()
    try:
        tables = {row["name"] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        recorded = {row["name"] for row in conn.execute("SELECT name FROM schema_migrations")}
    finally:
        conn.close()
    assert "locations" not in tables  # Teil vor dem Fehler wurde zurückgerollt
    assert recorded == {"001_init.sql"}

    (migrations / "002_broken.sql").write_text("CREATE TABLE locations (id INTEGER PRIMARY KEY);", encoding="utf-8")
    assert db.run_migrations() == ["002_broken.sql"]  # nach Korrektur wird sie angewendet


def test_database_from_old_runner_is_adopted(migrations):
    """Datenbanken aus der Zeit ohne schema_migrations: idempotente 001/002 laufen einmal nach und werden protokolliert."""
    init = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT);"
    seed = "INSERT OR IGNORE INTO items (id, name) VALUES (1, 'Beamer');"
    conn = sqlite3.connect(db.get_db_path())
    conn.executescript(init + seed)  # so hat der alte Runner die DB hinterlassen
    conn.close()
    (migrations / "001_init.sql").write_text(init, encoding="utf-8")
    (migrations / "002_seed.sql").write_text(seed, encoding="utf-8")

    assert db.run_migrations() == ["001_init.sql", "002_seed.sql"]
    assert db.run_migrations() == []
    conn = db.connect()
    try:
        assert conn.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 1
    finally:
        conn.close()
