from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.models.financial_record import FinancialRecord, RecordType
from app.schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordUpdate,
)


class RecordRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, record_id: int, user_id: int) -> Optional[FinancialRecord]:
        return self.db.query(FinancialRecord).filter(
            FinancialRecord.id == record_id,
            FinancialRecord.user_id == user_id,
            FinancialRecord.is_deleted.is_(False),
        ).first()

    def create(self, record_in: FinancialRecordCreate, user_id: int) -> FinancialRecord:
        record = FinancialRecord(
            amount=record_in.amount,
            type=record_in.type,
            category=record_in.category,
            date=record_in.date or datetime.utcnow(),
            notes=record_in.notes,
            user_id=user_id,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update(
        self,
        db_obj: FinancialRecord,
        obj_in: FinancialRecordUpdate,
    ) -> FinancialRecord:
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, record_id: int, user_id: int) -> Optional[FinancialRecord]:
        record = self.db.query(FinancialRecord).filter(
            FinancialRecord.id == record_id,
            FinancialRecord.user_id == user_id,
            FinancialRecord.is_deleted.is_(False),
        ).first()

        if record:
            record.is_deleted = True
            record.deleted_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(record)

        return record

    def restore(self, record_id: int, user_id: int) -> Optional[FinancialRecord]:
        """Restore a soft-deleted record."""
        record = self.db.query(FinancialRecord).filter(
            FinancialRecord.id == record_id,
            FinancialRecord.user_id == user_id,
            FinancialRecord.is_deleted.is_(True),
        ).first()

        if record:
            record.is_deleted = False
            record.deleted_at = None
            self.db.commit()
            self.db.refresh(record)

        return record

    def list(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        type: Optional[RecordType] = None,
        category: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ):
        query = self.db.query(FinancialRecord).filter(
            FinancialRecord.user_id == user_id,
            FinancialRecord.is_deleted.is_(False),
        )

        if type:
            query = query.filter(FinancialRecord.type == type)

        if category:
            query = query.filter(FinancialRecord.category == category)

        if start_date:
            query = query.filter(FinancialRecord.date >= start_date)

        if end_date:
            query = query.filter(FinancialRecord.date <= end_date)

        return (
            query.order_by(FinancialRecord.date.desc(), FinancialRecord.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )