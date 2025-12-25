from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.connection import get_db
from app.schemas.user import UserCreate, UserResponse, Token, RefreshTokenPayload
from app.core.exceptions import TokenExpiredError, InvalidTokenError
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_create: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    """Register a new user"""
    try:
        new_user = await AuthService.register_user(db, user_create)
        return UserResponse.model_validate(new_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> Token:
    try:
        return await AuthService.login_user(db, form_data.username, form_data.password)
    except ValueError as e:
        error_msg = str(e)
        if "inactive" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_msg
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg,
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenPayload,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> Token:
    try:
        return await AuthService.refresh_access_token(db, refresh_data.refresh_token)
    except (TokenExpiredError, InvalidTokenError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e) if isinstance(e, ValueError) else "Invalid or expired refresh token"
        )