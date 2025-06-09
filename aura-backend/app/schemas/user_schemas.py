from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID

# Schema for the payload (claims) of a JWT.
class TokenPayload(SQLModel):
    sub: Optional[str] = None

# Base model for User, containing common fields.
# This is not a table model.
class UserBase(SQLModel):
    email: str

# Schema for creating a user (e.g., in a POST request).
# It has fields that are required for creation.
class UserCreate(UserBase):
    password: str

# Schema for reading a user (e.g., in a GET response).
# This is also a table model, but we will rely on the main User model for tables.
# For now, let's treat this as a separate API model.
class UserRead(UserBase):
    id: UUID
    is_active: bool

# Schema for updating a user (e.g., in a PATCH request).
# All fields are optional.
class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None 