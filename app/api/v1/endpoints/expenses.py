from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models.expenses import Expense
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.db.session import get_db
from sqlalchemy import select
router = APIRouter()

# Create Expense


@router.post("", response_model=ExpenseResponse)
async def create_expense(expense: ExpenseCreate, db: AsyncSession = Depends(get_db)):
    new_expense = Expense(**expense.dict())
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return new_expense

# Get All Expenses


@router.get("", response_model=List[ExpenseResponse])
async def get_expenses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Expense).order_by(Expense.date_of_expense.desc().nullslast()))
    expenses = result.scalars().all()
    return expenses


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Expense).filter(Expense.id == expense_id))
    expense = result.scalars().first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense
