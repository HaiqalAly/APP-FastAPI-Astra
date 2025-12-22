from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from contextlib import asynccontextmanager

from app.db.connection import get_db, engine
from app.core.config import CONFIG

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