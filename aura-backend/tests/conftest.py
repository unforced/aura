import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
import os

from app.main import app
from app.db.session import get_db
from app.core.config import get_settings, Settings

# --- Test Environment Setup ---

def get_settings_override():
    # Point to the .env.test file
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env.test")
    return Settings(_env_file=env_file, TESTING=True)

# Override the get_settings dependency for all tests
app.dependency_overrides[get_settings] = get_settings_override

# Create a new engine for the test database
settings_override = get_settings_override()
engine = create_engine(str(settings_override.DATABASE_URL))

# --- Fixtures ---

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Fixture to set up the test database before any tests run
    and tear it down after all tests are done.
    """
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def session() -> Generator[Session, None, None]:
    """
    Provides a clean database session for each test function.
    Rolls back any changes after the test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    db_session = Session(bind=connection)

    yield db_session

    db_session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(session: Session) -> Generator[TestClient, None, None]:
    """
    Provides a TestClient that uses the test database session.
    """
    def get_db_override():
        return session

    app.dependency_overrides[get_db] = get_db_override
    
    with TestClient(app) as c:
        yield c

    # Clean up the override after the test
    app.dependency_overrides.pop(get_db, None)

@pytest.fixture(scope="function")
def authenticated_client(client: TestClient, session: Session) -> TestClient:
    """
    Provides a TestClient that is pre-authenticated as a test user.
    """
    from app.crud.crud_user import create_user
    from app.schemas.user_schemas import UserCreate

    # Create a test user
    test_email = "test.auth@example.com"
    test_password = "testpassword"
    user_in = UserCreate(email=test_email, password=test_password)
    create_user(db=session, user_in=user_in)

    # Log the user in to get a token
    login_data = {"username": test_email, "password": test_password}
    response = client.post(f"{get_settings().API_V1_STR}/login/access-token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Set the authorization header for the client
    client.headers["Authorization"] = f"Bearer {token}"

    return client 