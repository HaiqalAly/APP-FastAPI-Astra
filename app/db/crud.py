from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.models import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        is_active=True,
        role="user"
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None:
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user