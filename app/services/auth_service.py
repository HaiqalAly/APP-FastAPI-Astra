from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import crud
from app.db.models.models import User
from app.core.config import CONFIG
from app.core import security
from app.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError, InactiveUserError, InvalidTokenError
from app.schemas.user import UserCreate, Token


async def register_user(
    db: AsyncSession,
    user_create: UserCreate
) -> User:
    existing_user = await crud.get_user_by_username(db, user_create.username)
    if existing_user:
        raise UserAlreadyExistsError("username")
    existing_email = await crud.get_user_by_email(db, user_create.email)
    if existing_email:
        raise UserAlreadyExistsError("email")
    new_user = await crud.create_user(db, user_create)
    return new_user


async def login_user(db: AsyncSession, username: str, password: str) -> Token:
    user = await crud.authenticate_user(db, username, password)
    if not user:
        raise InvalidCredentialsError()
    if not user.is_active:
        raise InactiveUserError()
    
    access_token_expires = timedelta(minutes=CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=CONFIG.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token(
        data={"sub": user.username},
        expires_delta=refresh_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> Token:
    payload = security.verify_refresh_token(refresh_token)
    username: str | None = payload.get("sub")
    if not username:
        raise InvalidTokenError("Invalid refresh token")
    
    user = await crud.get_user_by_username(db, username)
    if not user:
        raise InvalidCredentialsError("User not found")
    if not user.is_active:
        raise InactiveUserError()
    
    access_token_expires = timedelta(minutes=CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return Token(
        access_token=new_access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )