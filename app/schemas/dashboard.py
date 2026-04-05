from pydantic import BaseModel, Field, ConfigDict
from typing import List

from app.schemas.financial_record import FinancialRecordResponse


class CategoryTotal(BaseModel):
    category: str
    total: float = Field(..., ge=0)


class TrendData(BaseModel):
    period: str
    income: float = Field(..., ge=0)
    expense: float = Field(..., ge=0)


class DashboardSummaryResponse(BaseModel):
    total_income: float = Field(..., ge=0)
    total_expense: float = Field(..., ge=0)
    net_balance: float = Field(...)

    category_wise_totals: List[CategoryTotal]
    recent_activity: List[FinancialRecordResponse]
    trends: List[TrendData]

    model_config = ConfigDict(from_attributes=True)