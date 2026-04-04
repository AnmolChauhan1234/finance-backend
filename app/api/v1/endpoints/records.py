from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialRecordResponse,
)
from app.services.record_service import record_service
from app.models.user import Role, User
from app.models.financial_record import RecordType


router = APIRouter()


@router.get("/", response_model=List[FinancialRecordResponse])
def read_records(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = Query(100, le=100),
    type: Optional[RecordType] = None,
    category: Optional[str] = None,
    current_user: User = Depends(deps.require_role([Role.ADMIN, Role.ANALYST])),
):
    records = record_service.list_records(
        db, skip=skip, limit=limit, type=type, category=category
    )
    return records


@router.post("/", response_model=FinancialRecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(
    *,
    db: Session = Depends(deps.get_db),
    record_in: FinancialRecordCreate,
    current_user: User = Depends(deps.require_role([Role.ADMIN])),
):
    record = record_service.create_record(
        db, record_in=record_in, user_id=current_user.id
    )
    return record


@router.put("/{record_id}", response_model=FinancialRecordResponse)
def update_record(
    *,
    db: Session = Depends(deps.get_db),
    record_id: int,
    record_in: FinancialRecordUpdate,
    current_user: User = Depends(deps.require_role([Role.ADMIN])),
):
    try:
        record = record_service.update_record(
            db, record_id=record_id, obj_in=record_in
        )
        return record
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{record_id}", response_model=FinancialRecordResponse)
def delete_record(
    *,
    db: Session = Depends(deps.get_db),
    record_id: int,
    current_user: User = Depends(deps.require_role([Role.ADMIN])),
):
    record = record_service.delete_record(db, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record