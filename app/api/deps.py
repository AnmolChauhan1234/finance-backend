# from typing import Generator
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# import jwt
# from sqlalchemy.orm import Session

# from app.core.config import settings
# from app.db.session import SessionLocal
# from app.models.user import User, Role
# from app.services.user_service import user_service
# from app.schemas.token import TokenPayload


# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_V1_STR}/auth/login"
# )


# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


# def get_current_user(
#     db: Session = Depends(get_db),
#     token: str = Depends(oauth2_scheme),
# ) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=["HS256"]
#         )
#         token_data = TokenPayload(**payload)

#         if token_data.sub is None:
#             raise credentials_exception

#     except jwt.InvalidTokenError:
#         raise credentials_exception

#     user = user_service.get_user_by_email(db, email=token_data.sub)

#     if not user:
#         raise credentials_exception

#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Inactive user",
#         )

#     return user


# def require_role(roles: list[Role]):
#     def role_checker(current_user: User = Depends(get_current_user)):
#         if current_user.role not in roles:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Not enough permissions",
#             )
#         return current_user

#     return role_checker










from typing import Generator, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User, Role
from app.schemas.token import TokenPayload
from app.repositories.user_repository import UserRepository
from app.repositories.record_repository import RecordRepository
from app.services.user_service import UserService
from app.services.record_service import RecordService
from app.services.dashboard_service import DashboardService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


# ---------------- DATABASE ----------------

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- REPOSITORIES ----------------

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_record_repo(db: Session = Depends(get_db)) -> RecordRepository:
    return RecordRepository(db)


# ---------------- SERVICES ----------------

def get_user_service(
    repo: UserRepository = Depends(get_user_repo),
) -> UserService:
    return UserService(repo)


def get_record_service(
    repo: RecordRepository = Depends(get_record_repo),
) -> RecordService:
    return RecordService(repo)


def get_dashboard_service(
    repo: RecordRepository = Depends(get_record_repo),
) -> DashboardService:
    return DashboardService(repo)


# ---------------- AUTH ----------------

def get_current_user(
    user_repo: UserRepository = Depends(get_user_repo),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)

        if not token_data.sub:
            raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = user_repo.get_by_email(email=token_data.sub)

    if not user:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


# ---------------- RBAC ----------------

def require_role(roles: list[Role]) -> Callable:
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user

    return role_checker