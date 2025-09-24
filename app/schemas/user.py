from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    role: Optional[str] = "Admin"


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
