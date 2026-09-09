from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to the Project Management API!"
    }

def test_register_invalid_data():
    response = client.post(
        "/auth/register",
        json={
            "name": "A",
            "email": "invalid-email",
            "password": "123"
        }
    )

    assert response.status_code == 422

def test_login_invalid_password():
    response = client.post(
        "/auth/login",
        json={
            "email": "your-test-user@example.com",
            "password": "wrong-password"
        }
    )

    assert response.status_code == 401

def test_get_me_without_token():
    response = client.get("/users/me")

    assert response.status_code == 401

def test_get_me_invalid_token():
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    assert response.status_code == 401