from sqlmodel import Field, Relationship, SQLModel, Column, DateTime
from typing import Optional, List
from datetime import datetime, timezone
import sqlalchemy as sa
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)

    documents: List["Document"] = Relationship(back_populates="owner")


class Document(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    file_name: str
    file_path: str # For local storage in MVP
    upload_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), default=sa.func.now(), nullable=False)
    )
    status: str = Field(default="PENDING") # e.g., PENDING, PROCESSING, COMPLETED, FAILED

    owner_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="documents") 