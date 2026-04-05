import logging

from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.models.user import Role

# Explicit imports for Alembic detection
from app.models.user import User
from app.models.financial_record import FinancialRecord

logger = logging.getLogger(__name__)


def init_db() -> None:
    db = SessionLocal()

    try:
        user_repo = UserRepository(db)
        user_service = UserService(user_repo)

        user = user_service.get_user_by_email("admin@example.com")

        if not user:
            user_in = UserCreate(
                email="admin@example.com",
                password="adminpassword",
                role=Role.ADMIN,
                is_active=True,
            )

            user_service.create_user(user_in)

            logger.info("Admin user created: admin@example.com / adminpassword")

    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
    logger.info("Database initialization completed.")