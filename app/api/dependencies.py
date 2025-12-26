from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_access_token
from app.core.exceptions import (
    InvalidCredentialsError,
    InactiveUserError,
    InsufficientPermissionsError,
)
from app.db.connection import get_db
from app.db.crud import get_user_by_username
from app.db.models.models import User
from app.schemas.user import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    payload = verify_access_token(token)
    username: str | None = payload.get("sub")
    if username is None:
        raise InvalidCredentialsError("Could not validate credentials")

    user = await get_user_by_username(db, username)
    if user is None:
        raise InvalidCredentialsError("User not found")
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise InactiveUserError()
    return current_user


def require_role(allowed_roles: list[UserRole]):
    role_names = ", ".join([role.value for role in allowed_roles])

    async def role_checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        if current_user.role not in [role.value for role in allowed_roles]:
            raise InsufficientPermissionsError(
                f"Operation requires one of the following roles: {role_names}"
            )
        return current_user

    return role_checker
