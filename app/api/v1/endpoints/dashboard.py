from fastapi import APIRouter, Depends

from app.api import deps
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard_service import DashboardService
from app.models.user import User


router = APIRouter()


@router.get("/summary", response_model=DashboardSummaryResponse)
def read_dashboard_summary(
    dashboard_service: DashboardService = Depends(deps.get_dashboard_service),
    current_user: User = Depends(deps.get_current_user),
):
    return dashboard_service.get_summary(user_id=current_user.id)