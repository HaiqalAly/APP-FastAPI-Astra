from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_active_user
from app.db.models.models import User
from app.db.connection import get_db
from app.db.crud import update_user, delete_user
from app.schemas.user import UserResponse, UserUpdate, DeleteAccountConfirmation
from app.core.security import verify_password
from app.core.exceptions import (
    InvalidPasswordConfirmationError,
    InvalidConfirmationTextError,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Get current authenticated user profile"""
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    updated_user = await update_user(db, current_user, user_update)
    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    confirmation: DeleteAccountConfirmation,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    if not verify_password(confirmation.password, current_user.hashed_password):
        raise InvalidPasswordConfirmationError()

    if (
        confirmation.confirm_text is not None
        and confirmation.confirm_text != "DELETE MY ACCOUNT"
    ):
        raise InvalidConfirmationTextError()

    await delete_user(db, current_user)
