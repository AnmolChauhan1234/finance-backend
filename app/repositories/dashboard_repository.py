from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Tuple

from app.models.financial_record import FinancialRecord, RecordType


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    # TOTALS

    def get_total_by_type(self, record_type: RecordType, user_id: int) -> float:
        total = (
            self.db.query(func.sum(FinancialRecord.amount))
            .filter(
                FinancialRecord.type == record_type,
                FinancialRecord.user_id == user_id,
                FinancialRecord.is_deleted.is_(False),
            )
            .scalar()
        )

        return float(total or 0.0)

    # CATEGORY TOTALS

    def get_category_totals(self, user_id: int) -> List[Tuple[str, float]]:
        results = (
            self.db.query(
                FinancialRecord.category,
                func.sum(FinancialRecord.amount),
            )
            .filter(
                FinancialRecord.user_id == user_id,
                FinancialRecord.is_deleted.is_(False),
            )
            .group_by(FinancialRecord.category)
            .all()
        )

        return [(category, float(total or 0.0)) for category, total in results]

    # RECENT ACTIVITY

    def get_recent_activity(self, user_id: int, limit: int = 10) -> List[FinancialRecord]:
        return (
            self.db.query(FinancialRecord)
            .filter(
                FinancialRecord.user_id == user_id,
                FinancialRecord.is_deleted.is_(False),
            )
            .order_by(FinancialRecord.date.desc())
            .limit(limit)
            .all()
        )

    # MONTHLY TRENDS

    def get_monthly_trends(
        self, user_id: int
    ) -> List[Tuple]:
        return (
            self.db.query(
                func.date_trunc("month", FinancialRecord.date).label("month"),
                FinancialRecord.type,
                func.sum(FinancialRecord.amount),
            )
            .filter(
                FinancialRecord.user_id == user_id,
                FinancialRecord.is_deleted.is_(False),
            )
            .group_by(
                func.date_trunc("month", FinancialRecord.date),
                FinancialRecord.type,
            )
            .order_by(func.date_trunc("month", FinancialRecord.date))
            .all()
        )