from sqlmodel import Session
from uuid import UUID
from typing import Optional

from app.schemas.document_schemas import DocumentCreate
from app.db.models_pg import Document as PGDocument

def create_document(session: Session, document_in: DocumentCreate, owner_id: UUID) -> PGDocument:
    db_document = PGDocument.model_validate(document_in, update={"owner_id": owner_id})
    session.add(db_document)
    session.commit()
    session.refresh(db_document)
    return db_document

def get_document(session: Session, document_id: UUID) -> Optional[PGDocument]:
    """
    Retrieves a document by its ID.
    """
    return session.get(PGDocument, document_id)

def update_document_status(session: Session, document: PGDocument, status: str) -> PGDocument:
    """
    Updates the status of a document.
    """
    document.status = status
    session.add(document)
    session.commit()
    session.refresh(document)
    return document 