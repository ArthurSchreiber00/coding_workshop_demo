"""JSON-API für Ausleihen."""
import sqlite3
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query

from app import config
from app.db import get_conn
from app.errors import ApiError
from app.repositories import items as items_repo
from app.repositories import loans as repo
from app.repositories import members as members_repo
from app.schemas import Loan, LoanCreate
from app.security import require_api_key

router = APIRouter(prefix="/api/loans", tags=["loans"])


def _parse_date(value: str) -> date:
    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ApiError(422, "invalid_date", f"Ungültiges Datum: {value}")


@router.get("", response_model=list[Loan])
def list_loans(open: bool = Query(default=False), conn: sqlite3.Connection = Depends(get_conn)):
    return repo.list_loans(conn, open_only=open)


@router.get("/{loan_id}", response_model=Loan)
def get_loan(loan_id: int, conn: sqlite3.Connection = Depends(get_conn)):
    loan = repo.get_loan(conn, loan_id)
    if not loan:
        raise ApiError(404, "loan_not_found", f"Ausleihe {loan_id} existiert nicht.")
    return loan


@router.post("", response_model=Loan, status_code=201, dependencies=[Depends(require_api_key)])
def create_loan(data: LoanCreate, conn: sqlite3.Connection = Depends(get_conn)):
    item = items_repo.get_item(conn, data.item_id)
    if not item:
        raise ApiError(404, "item_not_found", f"Gerät {data.item_id} existiert nicht.")
    if item["status"] != "available":
        raise ApiError(409, "item_not_available", f"Gerät '{item['name']}' ist nicht verfügbar.")
    if not members_repo.get_member(conn, data.member_id):
        raise ApiError(404, "member_not_found", f"Person {data.member_id} existiert nicht.")

    today = date.today()
    due = data.due_date or today + timedelta(days=config.DEFAULT_LOAN_DAYS)
    if due < today:
        raise ApiError(422, "due_date_in_past", "Rückgabedatum liegt in der Vergangenheit.")

    loan = repo.create_loan(conn, data.item_id, data.member_id, today.isoformat(), due.isoformat())
    items_repo.set_status(conn, data.item_id, "on_loan")
    return loan


@router.post("/{loan_id}/return", response_model=Loan, dependencies=[Depends(require_api_key)])
def return_loan(loan_id: int, conn: sqlite3.Connection = Depends(get_conn)):
    loan = repo.get_loan(conn, loan_id)
    if not loan:
        raise ApiError(404, "loan_not_found", f"Ausleihe {loan_id} existiert nicht.")
    if loan["returned_at"]:
        raise ApiError(409, "already_returned", "Ausleihe wurde bereits zurückgegeben.")
    updated = repo.mark_returned(conn, loan_id, date.today().isoformat())
    items_repo.set_status(conn, loan["item_id"], "available")
    return updated
