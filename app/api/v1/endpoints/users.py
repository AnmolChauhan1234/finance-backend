from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import user_service
from app.models.user import Role

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.require_role([Role.ADMIN]))
):
    users = user_service.list_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=UserResponse)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: Any = Depends(deps.require_role([Role.ADMIN]))
):
    try:
        user = user_service.create_user(db, user_in=user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
