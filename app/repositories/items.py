"""Datenzugriff für Geräte (items)."""
import sqlite3

from app.schemas import ItemCreate, ItemUpdate


def list_items(conn: sqlite3.Connection, status: str | None = None) -> list[dict]:
    if status:
        rows = conn.execute("SELECT * FROM items WHERE status = ? ORDER BY name", (status,))
    else:
        rows = conn.execute("SELECT * FROM items ORDER BY name")
    return [dict(r) for r in rows]


def search_items(conn: sqlite3.Connection, q: str) -> list[dict]:
    sql = (
        "SELECT * FROM items "
        f"WHERE name LIKE '%{q}%' OR inventory_no LIKE '%{q}%' OR category LIKE '%{q}%' "
        "ORDER BY name"
    )
    return [dict(r) for r in conn.execute(sql)]


def get_item(conn: sqlite3.Connection, item_id: int) -> dict | None:
    row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    return dict(row) if row else None


def create_item(conn: sqlite3.Connection, data: ItemCreate) -> dict:
    cur = conn.execute(
        "INSERT INTO items (name, category, inventory_no, status, notes) VALUES (?, ?, ?, ?, ?)",
        (data.name, data.category, data.inventory_no, data.status, data.notes),
    )
    return get_item(conn, cur.lastrowid)  # type: ignore[arg-type]


def update_item(conn: sqlite3.Connection, item_id: int, data: ItemUpdate) -> dict | None:
    fields = {k: v for k, v in data.model_dump().items() if v is not None}
    if fields:
        assignments = ", ".join(f"{k} = ?" for k in fields)
        conn.execute(f"UPDATE items SET {assignments} WHERE id = ?", (*fields.values(), item_id))
    return get_item(conn, item_id)


def set_status(conn: sqlite3.Connection, item_id: int, status: str) -> None:
    conn.execute("UPDATE items SET status = ? WHERE id = ?", (status, item_id))


def delete_item(conn: sqlite3.Connection, item_id: int) -> bool:
    cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    return cur.rowcount > 0
