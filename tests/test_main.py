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


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "name": "Database Test User",
            "email": "database-test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Database Test User"
    assert data["email"] == "database-test@example.com"
    assert "password" not in data


def test_register_duplicate_email():
    response = client.post(
        "/auth/register",
        json={
            "name": "Another User",
            "email": "database-test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 409


def test_login_database_user():
    response = client.post(
        "/auth/login",
        json={
            "email": "database-test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_me_database_user():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "database-test@example.com",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "database-test@example.com"
    assert data["name"] == "Database Test User"


def test_login_database_user_wrong_password():
    response = client.post(
        "/auth/login",
        json={
            "email": "database-test@example.com",
            "password": "wrong-password"
        }
    )

    assert response.status_code == 401