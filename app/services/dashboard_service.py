from app.models.financial_record import RecordType
from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, repo: DashboardRepository):
        self.repo = repo

    def get_summary(self, user_id: int):
        income = self.repo.get_total_by_type(RecordType.INCOME, user_id) or 0.0
        expense = self.repo.get_total_by_type(RecordType.EXPENSE, user_id) or 0.0

        net_balance = income - expense

        category_totals = self.repo.get_category_totals(user_id)
        recent_activity = self.repo.get_recent_activity(user_id)
        trend_query = self.repo.get_monthly_trends(user_id)

        trends_dict = {}

        for month_ts, r_type, total in trend_query:
            if not month_ts:
                continue

            month_str = month_ts.strftime("%Y-%m")

            if month_str not in trends_dict:
                trends_dict[month_str] = {
                    "period": month_str,
                    "income": 0.0,
                    "expense": 0.0,
                }

            if r_type == RecordType.INCOME:
                trends_dict[month_str]["income"] += total
            else:
                trends_dict[month_str]["expense"] += total

        trends = sorted(trends_dict.values(), key=lambda x: x["period"])

        return {
            "total_income": income,
            "total_expense": expense,
            "net_balance": net_balance,
            "category_wise_totals": [
                {"category": c, "total": t} for c, t in category_totals
            ],
            "recent_activity": recent_activity,
            "trends": trends,
        }