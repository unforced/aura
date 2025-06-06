from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import ValidationError
from neo4j import Session
from typing import Generator

from app.core.config import settings
from app.db.models_pg import User
from app.schemas.user_schemas import TokenPayload
from app.crud import crud_user
from app.db.session import get_db

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud_user.get_user_by_email(db, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_graph_session(request: Request) -> Generator[Session, None, None]:
    """
    Dependency to get a Neo4j session from the application state.
    """
    if not hasattr(request.app.state, "graph_db"):
        raise RuntimeError("GraphDB not found in application state. Is the lifespan manager correctly configured?")
    
    session = request.app.state.graph_db.get_session()
    try:
        yield session
    finally:
        if session:
            session.close() 