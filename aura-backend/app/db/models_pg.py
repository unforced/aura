from sqlmodel import Field, Relationship, SQLModel, Column, DateTime
from typing import Optional, List
from datetime import datetime
import sqlalchemy as sa

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)

    documents: List["Document"] = Relationship(back_populates="owner")


class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    file_path: str # For local storage in MVP
    upload_timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=sa.func.now())
    )
    status: str = Field(default="PENDING") # e.g., PENDING, PROCESSING, COMPLETED, FAILED

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="documents") 