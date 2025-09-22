from pydantic import BaseModel
from datetime import date, datetime
from pydantic import ConfigDict


class TolaBase(BaseModel):
    village_id: int
    tola_name: str
    tola_code: str
    created_at: datetime
    updated_at: datetime


class VillageOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class TolaOut(TolaBase):
    id: int
    village: VillageOut

    model_config = ConfigDict(from_attributes=True)
