from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.models.user import User


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, user_in: UserCreate) -> User:
        if self.repo.get_by_email(email=user_in.email):
            raise ValueError("Email already registered")

        hashed_password = get_password_hash(user_in.password)

        return self.repo.create(
            email=user_in.email,
            hashed_password=hashed_password,
            role=user_in.role,
            is_active=user_in.is_active,
        )

    def get_user_by_email(self, email: str) -> User | None:
        return self.repo.get_by_email(email=email)

    def list_users(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip=skip, limit=limit)