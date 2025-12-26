from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from contextlib import asynccontextmanager

from app.db.connection import get_db, engine
from app.core.config import CONFIG
from app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    InactiveUserError,
    TokenExpiredError,
    InvalidTokenError,
    InsufficientPermissionsError
)
from app.core import handlers
from app.api.v1.endpoints import auth, users

# Lifespan events to initialize the database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not CONFIG.SECRET_KEY:
        raise ValueError("SECRET_KEY is not set in the configuration.")
    print("Starting up...")
    yield
    print("Shutting down...")
    await engine.dispose()

app = FastAPI(
    lifespan=lifespan
)

# Register global exception handlers
app.add_exception_handler(UserAlreadyExistsError, handlers.user_already_exists_handler)
app.add_exception_handler(InvalidCredentialsError, handlers.invalid_credentials_handler)
app.add_exception_handler(InactiveUserError, handlers.inactive_user_handler)
app.add_exception_handler(InsufficientPermissionsError, handlers.insufficient_permissions_handler)
app.add_exception_handler(TokenExpiredError, handlers.token_expired_handler)
app.add_exception_handler(InvalidTokenError, handlers.invalid_token_handler)

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    """Test endpoint to verify database connection and session management"""
    result = await db.execute(text("SELECT 1 as test, current_database(), current_user"))
    row = result.first()
    if row is None:
        return {"status": "error", "message": "No result from database"}
    return {
        "status": "connected",
        "test_query": row[0],
        "database": row[1],
        "user": row[2],
        "session_closed": False 
    }

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")