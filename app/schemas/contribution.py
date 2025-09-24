from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class ContributionCreate(BaseModel):
    # Common fields
    receipt_id: str = Field(..., min_length=1,
                            description="Offline receipt ID")
    tola_id: int
    event_id: int
    payment_date: datetime
    amount: float
    payment_mode_id: int
    financial_year_id: int

    # New contributor toggle
    is_new_contributor: bool = False

    # Existing contributor
    contributor_id: Optional[int] = None

    # New contributor details
    contributor_name: Optional[str] = None
    father_or_spouse_name: Optional[str] = None
    contact: Optional[str] = None  # mobile number, optional

    @model_validator(mode="after")
    def validate_contributor(self):
        if self.is_new_contributor:
            if not self.contributor_name or not self.father_or_spouse_name:
                raise ValueError(
                    "contributor_name and father_or_spouse_name are required for new contributors"
                )
        else:
            if not self.contributor_id:
                raise ValueError(
                    "contributor_id is required for existing contributors")
        return self


class ContributionResponse(BaseModel):
    id: int
    amount: float
    payment_date: datetime
    tola_name: str
    contributor_name: str
    payment_mode: str

    class Config:
        from_attributes = True  # ✅ Pydantic v2 replacement for orm_mode


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
        from_attributes = True
