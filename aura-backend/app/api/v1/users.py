from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.user_schemas import UserRead
from app.db.models_pg import User

router = APIRouter()

@router.get("/me", response_model=UserRead)
def read_users_me(
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get current user.
    """
    return current_user 