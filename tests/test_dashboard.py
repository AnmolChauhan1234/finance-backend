from tests.utils import get_auth_token


def test_dashboard_summary(test_client):
    token = get_auth_token(test_client)

    response = test_client.get(
        "/api/v1/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_income" in data
    assert "total_expense" in data
    assert "net_balance" in data
    assert "category_wise_totals" in data
    assert "recent_activity" in data
    assert "trends" in data