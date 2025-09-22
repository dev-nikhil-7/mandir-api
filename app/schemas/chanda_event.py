from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ChandaEventBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    financial_year_id: int


class ChandaEventCreate(ChandaEventBase):
    pass


class ChandaEventResponse(ChandaEventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
