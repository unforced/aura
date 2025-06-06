from sqlmodel import Session, select
from typing import Optional
from app.db.models_pg import User
from app.schemas.user_schemas import UserCreate
from app.core.security import get_password_hash

def create_user(db: Session, *, user_in: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db: The database session.
        user_in: The user creation data (from API).

    Returns:
        The newly created user object.
    """
    # Create a dictionary of the data for the new user instance
    # Hash the password before storing it
    user_data = user_in.model_dump()
    user_data["hashed_password"] = get_password_hash(user_in.password)
    del user_data["password"] # Remove the plain password

    db_user = User(**user_data)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def get_user_by_email(db: Session, *, email: str) -> Optional[User]:
    """
    Get a user by email.

    Args:
        db: The database session.
        email: The email of the user to retrieve.

    Returns:
        The user object or None if not found.
    """
    return db.exec(select(User).where(User.email == email)).first() 