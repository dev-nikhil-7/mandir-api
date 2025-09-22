from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
# Base schema for shared fields


class ContributorBase(BaseModel):
    name: str
    contact: Optional[str]
    tola_id: int

# Schema for creating a new contributor
# Inherits from Base and is used for POST requests


class ContributorCreate(ContributorBase):
    pass

# Full schema for API responses
# This is used to return data from the database


class TolaOut(BaseModel):
    id: int
    tola_name: str

    model_config = ConfigDict(from_attributes=True)


class VillageOutX(BaseModel):
    id: int
    name: int
    model_config = ConfigDict(from_attributes=True)


class VillageOut(BaseModel):
    id: int
    amount: float
    financial_year: VillageOutX
    model_config = ConfigDict(from_attributes=True)


class Contributor(ContributorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tola: TolaOut
    pledges: list[VillageOut]

    # Configuration for ORM mode
    # This allows Pydantic to read data directly from the SQLAlchemy ORM model
    model_config = ConfigDict(from_attributes=True)


class ContributorWithPledge(ContributorBase):
    id: int
    pledge_amount: float = 0.0   # ✅ add current year pledge
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
