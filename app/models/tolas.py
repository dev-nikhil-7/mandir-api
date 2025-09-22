from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Tolas(Base):
    __tablename__ = "tolas"

    id = Column(Integer, primary_key=True, index=True)
    village_id = Column(Integer,  ForeignKey("villages.id"))
    tola_name = Column(String, nullable=False)
    tola_code = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())
    # relationship
    village = relationship("Village", back_populates="tolas")
    contributors = relationship("Contributor", back_populates="tola")
