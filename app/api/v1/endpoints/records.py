from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, Body

from app.api import deps
from app.schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialRecordResponse,
)
from app.services.record_service import RecordService
from app.models.user import Role, User
from app.models.financial_record import RecordType


router = APIRouter()


@router.get("/", response_model=List[FinancialRecordResponse])
def read_records(
    skip: int = 0,
    limit: int = Query(100, le=100),
    type: Optional[RecordType] = None,
    category: Optional[str] = None,
    current_user: User = Depends(deps.require_role([Role.ADMIN, Role.ANALYST])),
    record_service: RecordService = Depends(deps.get_record_service),
):
    return record_service.list_records(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        type=type,
        category=category,
    )


@router.post(
    "/",
    response_model=FinancialRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_record(
    record_in: FinancialRecordCreate = Body(...),  # FIX
    current_user: User = Depends(deps.require_role([Role.ADMIN])),
    record_service: RecordService = Depends(deps.get_record_service),
):
    return record_service.create_record(
        record_in=record_in,
        user_id=current_user.id,
    )


@router.put("/{record_id}", response_model=FinancialRecordResponse)
def update_record(
    record_id: int,
    record_in: FinancialRecordUpdate = Body(...),  # FIX
    current_user: User = Depends(deps.require_role([Role.ADMIN])),
    record_service: RecordService = Depends(deps.get_record_service),
):
    try:
        return record_service.update_record(
            record_id=record_id,
            user_id=current_user.id,
            obj_in=record_in,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{record_id}", response_model=FinancialRecordResponse)
def delete_record(
    record_id: int,
    current_user: User = Depends(deps.require_role([Role.ADMIN])),
    record_service: RecordService = Depends(deps.get_record_service),
):
    try:
        return record_service.delete_record(
            record_id=record_id,
            user_id=current_user.id,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Record not found")


@router.patch("/{record_id}/restore", response_model=FinancialRecordResponse)
def restore_record(
    record_id: int,
    current_user: User = Depends(deps.require_role([Role.ADMIN])),
    record_service: RecordService = Depends(deps.get_record_service),
):
    try:
        return record_service.restore_record(
            record_id=record_id,
            user_id=current_user.id,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Deleted record not found")