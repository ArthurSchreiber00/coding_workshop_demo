"""JSON-API für Personen."""
import sqlite3

from fastapi import APIRouter, Depends, Response

from app.db import get_conn
from app.errors import ApiError
from app.repositories import loans as loans_repo
from app.repositories import members as repo
from app.schemas import Loan, Member, MemberCreate
from app.security import require_api_key

router = APIRouter(prefix="/api/members", tags=["members"])


@router.get("", response_model=list[Member])
def list_members(conn: sqlite3.Connection = Depends(get_conn)):
    return repo.list_members(conn)


@router.get("/{member_id}", response_model=Member)
def get_member(member_id: int, conn: sqlite3.Connection = Depends(get_conn)):
    member = repo.get_member(conn, member_id)
    if not member:
        raise ApiError(404, "member_not_found", f"Person {member_id} existiert nicht.")
    return member


@router.get("/{member_id}/loans", response_model=list[Loan])
def member_loans(member_id: int, conn: sqlite3.Connection = Depends(get_conn)):
    if not repo.get_member(conn, member_id):
        raise ApiError(404, "member_not_found", f"Person {member_id} existiert nicht.")
    return loans_repo.list_loans_for_member(conn, member_id)


@router.post("", response_model=Member, status_code=201, dependencies=[Depends(require_api_key)])
def create_member(data: MemberCreate, conn: sqlite3.Connection = Depends(get_conn)):
    try:
        return repo.create_member(conn, data)
    except sqlite3.IntegrityError:
        raise ApiError(409, "email_taken", f"E-Mail {data.email} ist bereits registriert.")


@router.delete("/{member_id}", status_code=204)
def delete_member(member_id: int, conn: sqlite3.Connection = Depends(get_conn)):
    # Admin-Funktion: Person entfernen
    if not repo.delete_member(conn, member_id):
        raise ApiError(404, "member_not_found", f"Person {member_id} existiert nicht.")
    return Response(status_code=204)
