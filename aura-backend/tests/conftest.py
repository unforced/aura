import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from app.main import app
from app.db.session import get_db
from app.core.config import Settings

# --- Test Environment Setup ---

@pytest.fixture(scope='function', autouse=True)
def test_settings(monkeypatch):
    """
    Monkeypatches the application settings for each test function.
    """
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env.test")
    settings_override = Settings(_env_file=env_file, TESTING=True)
    
    monkeypatch.setattr("app.core.config.settings", settings_override)
    monkeypatch.setattr("app.db.session.settings", settings_override)
    monkeypatch.setattr("app.worker.settings", settings_override)
    
    return settings_override

@pytest.fixture(scope='function')
def test_engine(test_settings):
    """
    Creates a new engine for the test database for each test function.
    """
    return create_engine(str(test_settings.DATABASE_URL))

# --- Fixtures ---

@pytest.fixture(scope="function")
def setup_test_db(test_engine):
    """
    Fixture to set up the test database before each test function
    and tear it down after.
    """
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(scope="function")
def session(test_engine, setup_test_db) -> Generator[Session, None, None]:
    """
    Provides a clean database session for each test function.
    """
    connection = test_engine.connect()
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

    app.dependency_overrides.pop(get_db, None)

@pytest.fixture(scope="function")
def authenticated_client(client: TestClient, session: Session, test_settings) -> TestClient:
    """
    Provides a TestClient that is pre-authenticated as a test user.
    """
    from app.crud import crud_user
    from app.schemas.user_schemas import UserCreate

    test_email = "test.auth@example.com"
    test_password = "testpassword"
    user_in = UserCreate(email=test_email, password=test_password)
    crud_user.create_user(db=session, user_in=user_in)

    login_data = {"username": test_email, "password": test_password}
    response = client.post(f"{test_settings.API_V1_STR}/login/access-token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    client.headers["Authorization"] = f"Bearer {token}"

    return client

@pytest.fixture(scope="session")
def sample_pdf_path(tmp_path_factory):
    """
    Creates a simple dummy PDF file for testing and returns its path.
    """
    pdf_path = tmp_path_factory.mktemp("data") / "sample.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, "This is a test PDF document for Project Aura.")
    c.save()
    return str(pdf_path) 