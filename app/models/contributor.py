from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Contributor(Base):
    __tablename__ = "contributors"

    id = Column(Integer, primary_key=True)
    # Assuming this is a foreign key
    tola_id = Column(Integer, ForeignKey("tolas.id"))
    name = Column(String(100))
    contact = Column(String(15))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(), onupdate=func.now())
    # relationship
    tola = relationship("Tolas", back_populates="contributors")
    pledges = relationship("Pledge", back_populates="contributor")
