from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class FinancialYear(Base):
    __tablename__ = "financial_years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # Changed to String
    notes = Column(String)
    is_active = Column(Boolean, default=False)
    is_current = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=False), default=func.now())
    updated_at = Column(DateTime(timezone=False),
                        default=func.now(), onupdate=func.now())

    # Relationships
    pledges = relationship("Pledge", back_populates="financial_year")
    # in financial_year.py
    chanda_events = relationship(
        "ChandaEvent", back_populates="financial_year")
