from sqlmodel import Session
from app.db.models_pg import Document

def create_document(db: Session, *, file_name: str, file_path: str, user_id: int) -> Document:
    """
    Create a new document record in the database.

    Args:
        db: The database session.
        file_name: The original name of the uploaded file.
        file_path: The path where the file is stored.
        user_id: The ID of the user who owns the document.

    Returns:
        The newly created document object.
    """
    db_document = Document(file_name=file_name, file_path=file_path, user_id=user_id)
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return db_document 