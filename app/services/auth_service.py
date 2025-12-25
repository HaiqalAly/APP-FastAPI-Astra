from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import crud
from app.db.models.models import User
from app.core.config import CONFIG
from app.core import security
from app.schemas.user import UserCreate, Token

class AuthService:
    @staticmethod
    async def register_user(
        db: AsyncSession,
        user_create: UserCreate
    ) -> User:
        existing_user = await crud.get_user_by_username(db, user_create.username)
        if existing_user:
            raise ValueError("Username already registered")
        existing_email = await crud.get_user_by_email(db, user_create.email)
        if existing_email:
            raise ValueError("Email already registered")
        new_user = await crud.create_user(db, user_create)
        return new_user
    
    @staticmethod
    async def login_user(db: AsyncSession, username: str, password: str) -> Token:
        user = await crud.authenticate_user(db, username, password)
        if not user:
            raise ValueError("Incorrect username or password")
        if not user.is_active:
            raise ValueError("User account is inactive")
        
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
    
    @staticmethod
    async def refresh_access_token(db: AsyncSession, refresh_token: str) -> Token:
        payload = security.verify_refresh_token(refresh_token)
        username: str | None = payload.get("sub")
        if not username:
            raise ValueError("Invalid refresh token")
        
        user = await crud.get_user_by_username(db, username)
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")
        
        access_token_expires = timedelta(minutes=CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = security.create_access_token(data={"sub": user.username})

        return Token(
            access_token=new_access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )