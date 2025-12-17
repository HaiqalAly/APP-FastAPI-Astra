from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import CONFIG

DB_URL = f"postgresql+asyncpg://{CONFIG.POSTGRES_USER}:{CONFIG.POSTGRES_PASSWORD}@db/{CONFIG.POSTGRES_DB}"

engine = create_async_engine(
    url=DB_URL,
    echo=True,
)

async def init_db():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        print(result.scalar())
        print("Database connection initialized.") 