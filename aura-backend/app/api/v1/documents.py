import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.api import deps
from app.crud import crud_document
from app.schemas.document_schemas import DocumentCreate, DocumentCreateResponse
from app.db.models_pg import User
from app.core.config import settings
from sqlmodel import Session

router = APIRouter()

@router.post("/upload", response_model=DocumentCreateResponse, status_code=201)
def upload_document(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    file: UploadFile = File(...)
):
    """
    Upload a document for the current user.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided.")

    # Define the path for the uploaded file
    # Note: In a real application, you would add more robust filename sanitization
    # and handle potential file name collisions.
    upload_dir = Path(settings.UPLOADS_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True) # Ensure the directory exists
    file_path = upload_dir / file.filename

    # Save the file to the configured directory
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    # Create the document record in the database
    doc_in = DocumentCreate(file_name=file.filename, file_path=str(file_path))
    document = crud_document.create_document(
        session=db,
        document_in=doc_in,
        owner_id=current_user.id
    )

    return document 