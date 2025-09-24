from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, func, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True, index=True)
    tola_id = Column(Integer, ForeignKey("tolas.id"), nullable=False)
    contributor_id = Column(Integer, ForeignKey(
        "contributors.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("chanda_events.id"), nullable=False)
    payment_mode_id = Column(Integer, ForeignKey(
        "payment_modes.id"), nullable=False)
    financial_year_id = Column(Integer, ForeignKey(
        "financial_years.id"), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())
    receipt_id = Column(String(100))

    # Relationships
    tola = relationship("Tolas")
    contributor = relationship("Contributor")
    event = relationship("ChandaEvent")
    payment_mode = relationship("PaymentMode", back_populates="contributions")
