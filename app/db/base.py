from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User
from app.models.financial_record import FinancialRecord