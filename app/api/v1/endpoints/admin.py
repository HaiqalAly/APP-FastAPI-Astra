from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.dependencies import require_role
from app.db.models.models import User
from app.schemas.user import UserRole

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/admin-dashboard")
async def admin_dashboard(
    current_user: Annotated[User, Depends(require_role([UserRole.ADMIN]))],
):
    """Admin-only endpoint - requires ADMIN role"""
    return {
        "message": f"Welcome to admin dashboard, {current_user.username}!",
        "role": current_user.role,
        "access_level": "administrator",
    }