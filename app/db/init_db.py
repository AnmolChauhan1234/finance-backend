from sqlalchemy.orm import Session
import logging
from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.services.user_service import user_service
from app.models.user import Role

# Explicit imports for Alembic detection
from app.models.user import User
from app.models.financial_record import FinancialRecord

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:

    user = user_service.get_user_by_email(db, email="admin@example.com")

    if not user:
        user_in = UserCreate(
            email="admin@example.com",
            password="adminpassword",
            role=Role.ADMIN,
            is_active=True,
        )
        user_service.create_user(db, user_in=user_in)

        logger.info("Admin user created: admin@example.com / adminpassword")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db = SessionLocal()

    try:
        init_db(db)
        logger.info("Database initialization completed.")
    finally:
        db.close()