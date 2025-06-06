from sqlmodel import SQLModel
from datetime import datetime

# Schema for reading document metadata
class DocumentRead(SQLModel):
    id: int
    file_name: str
    upload_timestamp: datetime
    status: str
    user_id: int

# Schema for the response after creating a document
class DocumentCreateResponse(SQLModel):
    id: int
    file_name: str
    status: str 