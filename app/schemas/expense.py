from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ExpenseBase(BaseModel):
    event_id: Optional[int] = None
    financial_year_id: Optional[int] = None
    amount: float
    description: Optional[str] = None
    expense_type: Optional[str] = None
    paid_by: Optional[str] = None
    approved_by: Optional[str] = None
    payment_mode: Optional[str] = None
    date_of_expense: Optional[date] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
