from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard_service import dashboard_service
from app.models.user import User


router = APIRouter()


@router.get("/summary", response_model=DashboardSummaryResponse)
def read_dashboard_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return dashboard_service.get_summary(db, user_id=current_user.id)