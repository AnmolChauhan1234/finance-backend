from typing import Optional
from datetime import datetime

from app.repositories.record_repository import RecordRepository
from app.schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordUpdate,
)
from app.models.financial_record import RecordType, FinancialRecord


class RecordService:
    def __init__(self, repo: RecordRepository):
        self.repo = repo

    def create_record(
        self,
        record_in: FinancialRecordCreate,
        user_id: int,
    ) -> FinancialRecord:
        if record_in.date is None:
            record_in.date = datetime.utcnow()

        return self.repo.create(record_in, user_id)

    def update_record(
        self,
        record_id: int,
        user_id: int,
        obj_in: FinancialRecordUpdate,
    ) -> FinancialRecord:
        record = self.repo.get(record_id, user_id)

        if not record:
            raise ValueError("Record not found")

        return self.repo.update(record, obj_in)

    def delete_record(self, record_id: int, user_id: int):
        record = self.repo.delete(record_id, user_id)

        if not record:
            raise ValueError("Record not found")

        return record

    def get_record(
        self,
        record_id: int,
        user_id: int,
    ) -> Optional[FinancialRecord]:
        return self.repo.get(record_id, user_id)

    def list_records(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        type: Optional[RecordType] = None,
        category: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ):
        return self.repo.list(
            user_id=user_id,
            skip=skip,
            limit=limit,
            type=type,
            category=category,
            start_date=start_date,
            end_date=end_date,
        )