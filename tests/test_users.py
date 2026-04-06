from tests.utils import get_auth_token


def test_create_user(test_client):
    token = get_auth_token(test_client)

    response = test_client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "password": "test123",
            "role": "ANALYST",
            "is_active": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


def test_list_users(test_client):
    token = get_auth_token(test_client)

    response = test_client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


# RBAC awareness test (important)
def test_unauthorized_access_without_token(test_client):
    response = test_client.get("/api/v1/users")
    assert response.status_code == 401