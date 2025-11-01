from sqlalchemy import Column, Integer, String, Text, Date, DECIMAL, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
# assuming you have a database.py that defines Base
from app.db.base_class import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("chanda_events.id"), nullable=True)
    financial_year_id = Column(Integer, ForeignKey(
        "financial_years.id"), nullable=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(Text)
    expense_type = Column(String(50))
    paid_by = Column(String(100))
    approved_by = Column(String(100))
    payment_mode = Column(String(50))
    date_of_expense = Column(Date)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=func.now(), onupdate=func.now())
