"""JSON-API für Geräte."""
import sqlite3

from fastapi import APIRouter, Depends, Query, Response

from app.db import get_conn
from app.errors import ApiError
from app.repositories import items as repo
from app.schemas import Item, ItemCreate, ItemUpdate
from app.security import require_api_key

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("", response_model=list[Item])
def list_items(
    status: str | None = Query(default=None),
    q: str | None = Query(default=None, description="Suche in Name, Inventarnummer, Kategorie"),
    conn: sqlite3.Connection = Depends(get_conn),
):
    if q:
        return repo.search_items(conn, q)
    return repo.list_items(conn, status)


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, conn: sqlite3.Connection = Depends(get_conn)):
    item = repo.get_item(conn, item_id)
    if not item:
        raise ApiError(404, "item_not_found", f"Gerät {item_id} existiert nicht.")
    return item


@router.post("", response_model=Item, status_code=201, dependencies=[Depends(require_api_key)])
def create_item(data: ItemCreate, conn: sqlite3.Connection = Depends(get_conn)):
    try:
        return repo.create_item(conn, data)
    except sqlite3.IntegrityError:
        raise ApiError(409, "inventory_no_taken", f"Inventarnummer {data.inventory_no} ist bereits vergeben.")


@router.patch("/{item_id}", response_model=Item, dependencies=[Depends(require_api_key)])
def update_item(item_id: int, data: ItemUpdate, conn: sqlite3.Connection = Depends(get_conn)):
    if not repo.get_item(conn, item_id):
        raise ApiError(404, "item_not_found", f"Gerät {item_id} existiert nicht.")
    return repo.update_item(conn, item_id, data)


@router.delete("/{item_id}", status_code=204, dependencies=[Depends(require_api_key)])
def delete_item(item_id: int, conn: sqlite3.Connection = Depends(get_conn)):
    if not repo.delete_item(conn, item_id):
        raise ApiError(404, "item_not_found", f"Gerät {item_id} existiert nicht.")
    return Response(status_code=204)
