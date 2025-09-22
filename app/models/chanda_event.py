from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class ChandaEvent(Base):
    __tablename__ = 'chanda_events'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())
    financial_year_id = Column(Integer, ForeignKey(
        'financial_years.id'), nullable=False)

    # Relationships (assuming you have a FinancialYear model)
    financial_year = relationship(
        "FinancialYear", back_populates="chanda_events")
