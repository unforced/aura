from sqlmodel import SQLModel
from datetime import datetime
from uuid import UUID

# Schema for creating a document (internal, not directly from API)
class DocumentCreate(SQLModel):
    file_name: str
    file_path: str

# Schema for reading document metadata
class DocumentRead(SQLModel):
    id: UUID
    file_name: str
    upload_timestamp: datetime
    status: str
    owner_id: UUID

# Schema for the response after creating a document
class DocumentCreateResponse(SQLModel):
    id: UUID
    file_name: str
    status: str 