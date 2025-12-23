from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.dependencies import get_current_active_user, require_role
from app.db.models.models import User
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user