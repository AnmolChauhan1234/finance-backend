from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.base import Base


class RecordType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float, nullable=False)

    type = Column(
        Enum(RecordType, name="record_type_enum"),
        nullable=False
    )

    category = Column(String, index=True, nullable=False)

    date = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)

    notes = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="records")

    # Soft delete (with performance improvement)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime, nullable=True)

    # Debugging helper
    def __repr__(self):
        return f"<FinancialRecord id={self.id} amount={self.amount} type={self.type.value}>"