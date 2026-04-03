from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
import datetime
from app.db.base import Base

class RecordType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(RecordType), nullable=False)
    category = Column(String, index=True, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Note: Soft delete feature considerations.
    # To implement soft delete later as an enhancement, uncomment the following fields
    # and update query filters consistently to handle `is_deleted == False` states.
    # is_deleted = Column(Boolean, default=False)
    # deleted_at = Column(DateTime, nullable=True)

    user = relationship("User")
