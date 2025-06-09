from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
import shutil
from sqlmodel import Session

from app.api import deps
from app.crud import crud_document
from app.schemas.document_schemas import DocumentCreate, DocumentCreateResponse
from app.db.models_pg import User
from app.core.config import settings
from app.core.celery_app import celery_app

router = APIRouter()


@router.post("/upload", response_model=DocumentCreateResponse, status_code=201)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Upload a document for the authenticated user.
    """
    # Ensure the upload directory exists
    upload_dir = Path(settings.UPLOADS_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save the uploaded file
    file_path = upload_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create a document record in the database
    document_create = DocumentCreate(file_name=file.filename, file_path=str(file_path))
    document = crud_document.create_document(
        session=db, document_in=document_create, owner_id=current_user.id
    )

    # Dispatch the processing task to the Celery worker by name
    celery_app.send_task("app.worker.process_document_for_mvp", args=[str(document.id)])

    return document 