import pytest
import os
from typing import Generator
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.orm import sessionmaker

# Set the TESTING environment variable before importing app modules
os.environ["TESTING"] = "true"

from app.main import app
from app.api import deps
from app.core.config import settings
from app.db.models_pg import User, Document
from app.core.security import get_password_hash


# Use SQLite for testing to avoid external dependencies
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="db")
def db_fixture():
    """
    Pytest fixture for providing a test database session.
    """
    # Create all tables for the test database
    SQLModel.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test
        SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture(name="client")
def client_fixture(db: Session):
    """
    Pytest fixture for providing a FastAPI test client.
    """
    def get_db_override():
        return db

    app.dependency_overrides[deps.get_db] = get_db_override
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(db: Session) -> User:
    """
    Creates a test user for authentication tests.
    """
    user_in = {
        "email": "test@example.com",
        "password": get_password_hash("password"),
    }
    user = User(**user_in)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(client: TestClient, test_user: User) -> dict:
    """
    Provides authentication headers for API requests.
    """
    login_data = {
        "username": test_user.email,
        "password": "password",  # Use the plain password here
    }
    response = client.post("/api/v1/login/access-token", data=login_data)
    tokens = response.json()
    access_token = tokens["access_token"]
    return {"Authorization": f"Bearer {access_token}"} 