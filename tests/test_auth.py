def test_login_success(test_client):
    response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@example.com",
            "password": "adminpassword",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_fail(test_client):
    response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401