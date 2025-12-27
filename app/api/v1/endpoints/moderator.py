from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.dependencies import require_role
from app.db.models.models import User
from app.schemas.user import UserRole

router = APIRouter(prefix="/moderator", tags=["moderator"])


@router.get("/moderator-panel")
async def moderator_panel(
    current_user: Annotated[
        User, Depends(require_role([UserRole.ADMIN, UserRole.MODERATOR]))
    ],
):
    """Moderator and Admin access - requires MODERATOR or ADMIN role"""
    return {
        "message": f"Welcome to moderator panel, {current_user.username}!",
        "role": current_user.role,
        "access_level": "moderator or higher",
    }
