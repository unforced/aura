from sqlmodel import SQLModel
from datetime import datetime
from uuid import UUID
from typing import List, Dict, Any

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

# Schema for querying a document
class DocumentQueryRequest(SQLModel):
    question: str

# Schema for the response after querying a document
class DocumentQueryResponse(SQLModel):
    answer: str
    chunks_used: List[Dict[str, Any]] 