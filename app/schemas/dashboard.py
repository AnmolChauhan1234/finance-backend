from pydantic import BaseModel, Field, ConfigDict
from typing import List

from app.schemas.financial_record import FinancialRecordResponse


class CategoryTotal(BaseModel):
    category: str
    total: float = Field(..., ge=0)


class TrendData(BaseModel):
    period: str  # e.g. "2026-04"
    income: float = Field(..., ge=0)
    expense: float = Field(..., ge=0)


class DashboardSummaryResponse(BaseModel):
    total_income: float = Field(..., ge=0)
    total_expense: float = Field(..., ge=0)

    # Better validation
    net_balance: float = Field(
        ...,
        description="Income - Expense (can be negative)"
    )

    category_wise_totals: List[CategoryTotal]
    recent_activity: List[FinancialRecordResponse]
    trends: List[TrendData]

    model_config = ConfigDict(from_attributes=True)