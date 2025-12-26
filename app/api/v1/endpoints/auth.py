from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.connection import get_db
from app.schemas.user import UserCreate, UserResponse, Token, RefreshTokenPayload
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_create: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    """Register a new user"""
    new_user = await auth_service.register_user(db, user_create)
    return UserResponse.model_validate(new_user)


@router.post("/login", response_model=Token)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    """Login user and return access/refresh tokens"""
    return await auth_service.login_user(db, form_data.username, form_data.password)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenPayload, db: Annotated[AsyncSession, Depends(get_db)]
) -> Token:
    """Refresh access token using refresh token"""
    return await auth_service.refresh_access_token(db, refresh_data.refresh_token)
