from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class ContributionBase(BaseModel):
    tola_id: int
    contributor_id: int
    event_id: int
    payment_date: datetime
    amount: float
    payment_mode_id: int
    financial_year_id: int


class ContributionCreate(ContributionBase):
    pass


class ContributionResponse(ContributionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ContributionResponse(BaseModel):
    id: int
    amount: float
    payment_date: datetime

    # joined fields
    tola_name: str
    contributor_name: str
    payment_mode: str

    class Config:
        orm_mode = True


class ContributionCreateResponse(BaseModel):
    id: int
    tola_id: int
    contributor_id: int
    event_id: int
    payment_mode_id: int
    payment_date: datetime
    amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
