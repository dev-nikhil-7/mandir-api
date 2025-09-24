from sqlalchemy import Column, Integer, String, Numeric, DateTime, func, ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Pledge(Base):
    __tablename__ = "pledges"

    id = Column(Integer, primary_key=True)
    contributor_id = Column(Integer, ForeignKey("contributors.id"))
    financial_year_id = Column(Integer, ForeignKey("financial_years.id"))
    amount = Column(Numeric(12, 2))
    notes = Column(String)
    created_at = Column(DateTime(timezone=False), default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now()
    )
    # Relationships
    contributor = relationship("Contributor", back_populates="pledges")
    financial_year = relationship("FinancialYear", back_populates="pledges")
