from sqlalchemy import Column, Integer, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class PaymentMode(Base):
    __tablename__ = "payment_modes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)

    contributions = relationship("Contribution", back_populates="payment_mode")
