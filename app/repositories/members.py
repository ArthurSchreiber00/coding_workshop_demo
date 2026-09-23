"""Datenzugriff für Personen (members)."""
import sqlite3

from app.schemas import MemberCreate


def list_members(conn: sqlite3.Connection) -> list[dict]:
    return [dict(r) for r in conn.execute("SELECT * FROM members ORDER BY name")]


def search_members(conn: sqlite3.Connection, q: str) -> list[dict]:
    pattern = f"%{q}%"
    rows = conn.execute(
        "SELECT * FROM members WHERE name LIKE ? OR email LIKE ? OR team LIKE ? ORDER BY name",
        (pattern, pattern, pattern),
    )
    return [dict(r) for r in rows]


def get_member(conn: sqlite3.Connection, member_id: int) -> dict | None:
    row = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
    return dict(row) if row else None


def create_member(conn: sqlite3.Connection, data: MemberCreate) -> dict:
    cur = conn.execute(
        "INSERT INTO members (name, email, team, is_admin) VALUES (?, ?, ?, ?)",
        (data.name, data.email, data.team, int(data.is_admin)),
    )
    return get_member(conn, cur.lastrowid)  # type: ignore[arg-type]


def delete_member(conn: sqlite3.Connection, member_id: int) -> bool:
    cur = conn.execute("DELETE FROM members WHERE id = ?", (member_id,))
    return cur.rowcount > 0
