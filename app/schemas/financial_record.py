from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime

from app.models.financial_record import RecordType


class FinancialRecordBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: RecordType
    category: str = Field(..., min_length=1, max_length=100)
    notes: Optional[str] = None

    # FIX: normalize enum input
    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v


class FinancialRecordCreate(FinancialRecordBase):
    date: Optional[datetime] = None


class FinancialRecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    date: Optional[datetime] = None
    notes: Optional[str] = None

    # FIX here also
    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v


class FinancialRecordResponse(BaseModel):
    id: int
    amount: float
    type: RecordType
    category: str
    date: datetime
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)