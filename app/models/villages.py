from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Village(Base):
    __tablename__ = "villages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())

    tolas = relationship("Tolas", back_populates="village")
