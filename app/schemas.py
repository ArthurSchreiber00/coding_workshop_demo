"""Request- und Response-Modelle (Pydantic)."""
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

ItemStatus = Literal["available", "on_loan", "maintenance"]


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=60)
    inventory_no: str = Field(min_length=1, max_length=30)
    status: ItemStatus = "available"
    notes: str | None = None


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    category: str | None = Field(default=None, min_length=1, max_length=60)
    status: ItemStatus | None = None
    notes: str | None = None


class Item(ItemCreate):
    id: int
    created_at: str


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=3, max_length=200)
    team: str = Field(min_length=1, max_length=60)
    is_admin: bool = False


class Member(MemberCreate):
    id: int


class LoanCreate(BaseModel):
    item_id: int
    member_id: int
    due_date: date | None = None


class Loan(BaseModel):
    id: int
    item_id: int
    member_id: int
    loaned_at: date
    due_date: date
    returned_at: date | None = None
    item_name: str | None = None
    member_name: str | None = None


class ErrorBody(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorBody
