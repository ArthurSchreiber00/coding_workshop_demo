"""Datenzugriff für Ausleihen (loans)."""
import sqlite3

_BASE_SELECT = """
    SELECT l.*, i.name AS item_name, m.name AS member_name
    FROM loans l
    JOIN items   i ON i.id = l.item_id
    JOIN members m ON m.id = l.member_id
"""


def list_loans(conn: sqlite3.Connection, open_only: bool = False) -> list[dict]:
    sql = _BASE_SELECT
    if open_only:
        sql += " WHERE l.returned_at IS NULL"
    sql += " ORDER BY l.due_date, l.id"
    return [dict(r) for r in conn.execute(sql)]


def list_loans_for_member(conn: sqlite3.Connection, member_id: int) -> list[dict]:
    sql = _BASE_SELECT + " WHERE l.member_id = ? ORDER BY l.due_date DESC"
    return [dict(r) for r in conn.execute(sql, (member_id,))]


def get_loan(conn: sqlite3.Connection, loan_id: int) -> dict | None:
    row = conn.execute(_BASE_SELECT + " WHERE l.id = ?", (loan_id,)).fetchone()
    return dict(row) if row else None


def count_open_loans(conn: sqlite3.Connection, member_id: int) -> int:
    row = conn.execute(
        "SELECT COUNT(*) AS n FROM loans WHERE member_id = ? AND returned_at IS NULL", (member_id,)
    ).fetchone()
    return int(row["n"])


def create_loan(conn: sqlite3.Connection, item_id: int, member_id: int, loaned_at: str, due_date: str) -> dict:
    cur = conn.execute(
        "INSERT INTO loans (item_id, member_id, loaned_at, due_date) VALUES (?, ?, ?, ?)",
        (item_id, member_id, loaned_at, due_date),
    )
    return get_loan(conn, cur.lastrowid)  # type: ignore[arg-type]


def mark_returned(conn: sqlite3.Connection, loan_id: int, returned_at: str) -> dict | None:
    conn.execute("UPDATE loans SET returned_at = ? WHERE id = ?", (returned_at, loan_id))
    return get_loan(conn, loan_id)
