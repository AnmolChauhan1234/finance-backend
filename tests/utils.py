def get_auth_token(client):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@example.com",
            "password": "adminpassword",
        },
    )
    return response.json()["access_token"]