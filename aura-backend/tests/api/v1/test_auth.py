from fastapi.testclient import TestClient
from sqlmodel import Session
from app.core.config import get_settings

def test_create_user_success(client: TestClient, session: Session):
    """
    Test successful user creation.
    """
    email = "test.create@example.com"
    password = "testpassword123"
    response = client.post(
        f"{get_settings().API_V1_STR}/users/",
        json={"email": email, "password": password},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert "id" in data
    assert "is_active" in data
    assert data["is_active"] is True
    assert "hashed_password" not in data

def test_create_user_duplicate_email(client: TestClient, session: Session):
    """
    Test user creation with a duplicate email address.
    """
    email = "test.duplicate@example.com"
    password = "testpassword123"
    # Create the first user
    client.post(f"{get_settings().API_V1_STR}/users/", json={"email": email, "password": password})
    
    # Attempt to create a second user with the same email
    response = client.post(
        f"{get_settings().API_V1_STR}/users/",
        json={"email": email, "password": "anotherpassword"},
    )
    assert response.status_code == 400
    data = response.json()
    assert "already exists" in data["detail"]

def test_login_for_access_token_success(client: TestClient, session: Session):
    """
    Test successful login and token generation.
    """
    email = "test.login@example.com"
    password = "testpassword123"
    # Create a user first
    client.post(f"{get_settings().API_V1_STR}/users/", json={"email": email, "password": password})

    # Attempt to log in
    login_data = {"username": email, "password": password}
    response = client.post(f"{get_settings().API_V1_STR}/login/access-token", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_for_access_token_incorrect_password(client: TestClient, session: Session):
    """
    Test login with an incorrect password.
    """
    email = "test.login.fail@example.com"
    password = "testpassword123"
    # Create a user
    client.post(f"{get_settings().API_V1_STR}/users/", json={"email": email, "password": password})

    # Attempt to log in with the wrong password
    login_data = {"username": email, "password": "wrongpassword"}
    response = client.post(f"{get_settings().API_V1_STR}/login/access-token", data=login_data)
    assert response.status_code == 401
    data = response.json()
    assert "Incorrect email or password" in data["detail"] 