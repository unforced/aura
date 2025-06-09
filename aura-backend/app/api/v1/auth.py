from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.crud import crud_user
from app.schemas.user_schemas import UserCreate, UserRead
from app.db.session import get_db
from app.core.security import create_access_token, verify_password
from sqlmodel import SQLModel

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserRead, status_code=201)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
):
    """
    Register a new user.
    """
    try:
        user = crud_user.create_user(db=db, user_in=user_in)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    return user

@router.post("/users/", response_model=UserRead, status_code=201)
def register_user_legacy(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
):
    """
    Create a new user (legacy endpoint).
    """
    try:
        user = crud_user.create_user(db=db, user_in=user_in)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    return user 