from tests.utils import get_auth_token


def test_create_record(test_client):
    token = get_auth_token(test_client)

    response = test_client.post(
        "/api/v1/records",
        json={
            "amount": 1000,
            "type": "INCOME",
            "category": "Salary",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201


def test_get_records(test_client):
    token = get_auth_token(test_client)

    response = test_client.get(
        "/api/v1/records",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


# Validation test
def test_invalid_record_amount(test_client):
    token = get_auth_token(test_client)

    response = test_client.post(
        "/api/v1/records",
        json={
            "amount": -100,
            "type": "INCOME",
            "category": "Salary",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422