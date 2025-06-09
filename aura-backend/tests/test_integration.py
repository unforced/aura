import os
os.environ["TESTING"] = "True"
from fastapi.testclient import TestClient
from app.main import app

def test_app_basic_functionality():
    """Basic integration test for core functionality"""
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200
    # Test that upload endpoint exists (will return 401 without auth)
    files = {"file": ("test.txt", "test content", "text/plain")}
    response = client.post("/api/v1/documents/upload", files=files)
    assert response.status_code == 401  # Expected: Unauthorized
