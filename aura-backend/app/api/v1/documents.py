from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
import shutil
from sqlmodel import Session
from uuid import UUID

from app.api import deps
from app.crud import crud_document
from app.schemas.document_schemas import DocumentCreate, DocumentCreateResponse, DocumentQueryRequest, DocumentQueryResponse
from app.db.models_pg import User
from app.core.config import settings
from app.core.celery_app import celery_app
# from app.services.rag_service import RAGService  # Temporarily commented out due to import issues

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


@router.post("/{document_id}/query", response_model=DocumentQueryResponse)
def query_document(
    document_id: UUID,
    query_request: DocumentQueryRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Query a document using RAG (Retrieval-Augmented Generation).
    
    This endpoint retrieves relevant text chunks from the specified document
    and uses an LLM to generate a contextual answer to the user's question.
    """
    # 1. Verify the document exists and belongs to the current user
    document = crud_document.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this document")
    
    # 2. Check if document processing is complete
    if document.status != "COMPLETED":
        raise HTTPException(
            status_code=400, 
            detail=f"Document is not ready for querying. Current status: {document.status}"
        )
    
    # 3. Temporary mock implementation for demonstration
    # TODO: Replace with actual RAG service once import issues are resolved
    try:
        from app.services.rag_service import RAGService
        rag_service = RAGService()
        rag_response = rag_service.generate_answer(
            question=query_request.question,
            document_id=document_id
        )
        return DocumentQueryResponse(
            answer=rag_response.answer,
            chunks_used=rag_response.chunks_used
        )
    except ImportError:
        # Fallback mock response for demonstration
        return DocumentQueryResponse(
            answer=f"Mock answer for question: '{query_request.question}' about document '{document.file_name}'. (RAG service not available in current environment)",
            chunks_used=[
                {
                    "text": "This is a mock chunk from the document.",
                    "metadata": {"document_id": str(document_id), "chunk_index": 0},
                    "distance": 0.1
                }
            ]
        ) 