"""HTML-Seiten (Jinja2)."""
import os
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app import config
from app.db import get_conn
from app.repositories import items as items_repo
from app.repositories import loans as loans_repo
from app.repositories import members as members_repo

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

SHOW_DEBUG_FOOTER = os.getenv("TOOLSHED_DEBUG", "1") == "1"


def _parse_date(value: str) -> date | None:
    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def _render(request: Request, conn: sqlite3.Connection, template: str, **context) -> HTMLResponse:
    open_count = conn.execute("SELECT COUNT(*) FROM loans WHERE returned_at IS NULL").fetchone()[0]
    base = {
        "request": request,
        "app_name": config.APP_NAME,
        "open_count": open_count,
        "today": date.today().isoformat(),
        "show_debug": SHOW_DEBUG_FOOTER,
        "db_path": config.DB_PATH,
    }
    return templates.TemplateResponse(request, template, {**base, **context})


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, conn: sqlite3.Connection = Depends(get_conn)):
    stats = {
        "items": conn.execute("SELECT COUNT(*) FROM items").fetchone()[0],
        "available": conn.execute("SELECT COUNT(*) FROM items WHERE status = 'available'").fetchone()[0],
        "on_loan": conn.execute("SELECT COUNT(*) FROM items WHERE status = 'on_loan'").fetchone()[0],
        "members": conn.execute("SELECT COUNT(*) FROM members").fetchone()[0],
    }
    recent = conn.execute(
        "SELECT l.id, l.loaned_at, l.due_date, l.returned_at, i.name AS item_name, m.name AS member_name "
        "FROM loans l JOIN items i ON i.id = l.item_id JOIN members m ON m.id = l.member_id "
        "ORDER BY l.id DESC LIMIT 5"
    ).fetchall()
    return _render(request, conn, "index.html", stats=stats, recent=[dict(r) for r in recent])


@router.get("/items", response_class=HTMLResponse)
def items_page(request: Request, q: str = "", conn: sqlite3.Connection = Depends(get_conn)):
    items = items_repo.search_items(conn, q) if q else items_repo.list_items(conn)
    return _render(request, conn, "items.html", items=items, q=q)


@router.get("/items/new", response_class=HTMLResponse)
def new_item_form(request: Request, conn: sqlite3.Connection = Depends(get_conn)):
    return _render(request, conn, "item_form.html", error=None, form={})


@router.post("/items/new")
def create_item_form(
    request: Request,
    name: str = Form(...),
    category: str = Form(...),
    inventory_no: str = Form(...),
    notes: str = Form(""),
    conn: sqlite3.Connection = Depends(get_conn),
):
    from app.schemas import ItemCreate

    try:
        items_repo.create_item(conn, ItemCreate(name=name, category=category, inventory_no=inventory_no, notes=notes or None))
    except sqlite3.IntegrityError:
        return _render(
            request, conn, "item_form.html",
            error=f"Inventarnummer {inventory_no} ist bereits vergeben.",
            form={"name": name, "category": category, "inventory_no": inventory_no, "notes": notes},
        )
    return RedirectResponse(url="/items", status_code=303)


@router.get("/loans", response_class=HTMLResponse)
def loans_page(request: Request, conn: sqlite3.Connection = Depends(get_conn)):
    return _render(
        request, conn, "loans.html",
        loans=loans_repo.list_loans(conn),
        available_items=items_repo.list_items(conn, "available"),
        members=members_repo.list_members(conn),
        error=None,
        default_due=(date.today() + timedelta(days=config.DEFAULT_LOAN_DAYS)).isoformat(),
    )


@router.post("/loans/new")
def create_loan_form(
    request: Request,
    item_id: int = Form(...),
    member_id: int = Form(...),
    due_date: str = Form(""),
    conn: sqlite3.Connection = Depends(get_conn),
):
    error = None
    item = items_repo.get_item(conn, item_id)
    member = members_repo.get_member(conn, member_id)
    due = _parse_date(due_date) if due_date else date.today() + timedelta(days=config.DEFAULT_LOAN_DAYS)

    if not item or item["status"] != "available":
        error = "Das Gerät ist nicht verfügbar."
    elif not member:
        error = "Die Person existiert nicht."
    elif due is None:
        error = "Ungültiges Rückgabedatum."
    elif loans_repo.count_open_loans(conn, member_id) >= config.MAX_OPEN_LOANS_PER_MEMBER:
        error = f"{member['name']} hat bereits {config.MAX_OPEN_LOANS_PER_MEMBER} offene Ausleihen."

    if error:
        return _render(
            request, conn, "loans.html",
            loans=loans_repo.list_loans(conn),
            available_items=items_repo.list_items(conn, "available"),
            members=members_repo.list_members(conn),
            error=error,
            default_due=(date.today() + timedelta(days=config.DEFAULT_LOAN_DAYS)).isoformat(),
        )

    loans_repo.create_loan(conn, item_id, member_id, date.today().isoformat(), due.isoformat())  # type: ignore[union-attr]
    items_repo.set_status(conn, item_id, "on_loan")
    return RedirectResponse(url="/loans", status_code=303)


@router.post("/loans/{loan_id}/return")
def return_loan_form(loan_id: int, conn: sqlite3.Connection = Depends(get_conn)):
    loan = loans_repo.get_loan(conn, loan_id)
    if loan and not loan["returned_at"]:
        loans_repo.mark_returned(conn, loan_id, date.today().isoformat())
        items_repo.set_status(conn, loan["item_id"], "available")
    return RedirectResponse(url="/loans", status_code=303)


@router.get("/members", response_class=HTMLResponse)
def members_page(request: Request, conn: sqlite3.Connection = Depends(get_conn)):
    members = members_repo.list_members(conn)
    for m in members:
        m["open_loans"] = loans_repo.count_open_loans(conn, m["id"])
    return _render(request, conn, "members.html", members=members)
