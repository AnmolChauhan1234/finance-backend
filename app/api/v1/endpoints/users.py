from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api import deps
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import UserService
from app.models.user import Role, User


router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = Query(100, le=100),
    current_user: User = Depends(deps.require_role([Role.ADMIN])),
    user_service: UserService = Depends(deps.get_user_service),
):
    return user_service.list_users(skip=skip, limit=limit)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_in: UserCreate,
    current_user: User = Depends(deps.require_role([Role.ADMIN])),
    user_service: UserService = Depends(deps.get_user_service),
):
    try:
        return user_service.create_user(user_in=user_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )