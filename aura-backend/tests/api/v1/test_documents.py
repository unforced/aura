from fastapi.testclient import TestClient
from sqlmodel import Session
from io import BytesIO

def test_upload_document_success(authenticated_client: TestClient, session: Session):
    """
    Test successful document upload for an authenticated user.
    """
    # Create a dummy file in memory
    dummy_file_content = b"This is a test document."
    file_data = {"file": ("test_document.txt", BytesIO(dummy_file_content), "text/plain")}
    
    response = authenticated_client.post("/api/v1/documents/upload", files=file_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["file_name"] == "test_document.txt"
    assert data["status"] == "PENDING"
    assert "id" in data

def test_upload_document_unauthenticated(client: TestClient, session: Session):
    """
    Test that document upload fails for an unauthenticated user.
    """
    dummy_file_content = b"This should not be uploaded."
    file_data = {"file": ("unauth_test.txt", BytesIO(dummy_file_content), "text/plain")}

    response = client.post("/api/v1/documents/upload", files=file_data)
    
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authenticated" 