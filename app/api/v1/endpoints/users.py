from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.dependencies import get_current_active_user, require_role
from app.db.models.models import User
from app.schemas.user import UserResponse, UserRole

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Get current authenticated user profile"""
    return current_user

@router.get("/admin-dashboard")
async def admin_dashboard(
    current_user: Annotated[User, Depends(require_role([UserRole.ADMIN]))]
):
    """Admin-only endpoint - requires ADMIN role"""
    return {
        "message": f"Welcome to admin dashboard, {current_user.username}!",
        "role": current_user.role,
        "access_level": "administrator"
    }

@router.get("/moderator-panel")
async def moderator_panel(
    current_user: Annotated[User, Depends(require_role([UserRole.ADMIN, UserRole.MODERATOR]))]
):
    """Moderator and Admin access - requires MODERATOR or ADMIN role"""
    return {
        "message": f"Welcome to moderator panel, {current_user.username}!",
        "role": current_user.role,
        "access_level": "moderator or higher"
    }