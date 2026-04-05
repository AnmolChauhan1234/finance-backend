from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.financial_record import FinancialRecord, RecordType


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_total_by_type(self, record_type: RecordType, user_id: int) -> float:
        return (
            self.db.query(func.sum(FinancialRecord.amount))
            .filter(
                FinancialRecord.type == record_type,
                FinancialRecord.user_id == user_id
            )
            .scalar()
            or 0.0
        )

    def get_category_totals(self, user_id: int):
        return (
            self.db.query(
                FinancialRecord.category,
                func.sum(FinancialRecord.amount)
            )
            .filter(FinancialRecord.user_id == user_id)
            .group_by(FinancialRecord.category)
            .all()
        )

    def get_recent_activity(self, user_id: int, limit: int = 10):
        return (
            self.db.query(FinancialRecord)
            .filter(FinancialRecord.user_id == user_id)
            .order_by(FinancialRecord.date.desc())
            .limit(limit)
            .all()
        )

    def get_monthly_trends(self, user_id: int):
        return (
            self.db.query(
                func.date_trunc('month', FinancialRecord.date).label('month'),
                FinancialRecord.type,
                func.sum(FinancialRecord.amount)
            )
            .filter(FinancialRecord.user_id == user_id)
            .group_by(
                func.date_trunc('month', FinancialRecord.date),
                FinancialRecord.type
            )
            .all()
        )