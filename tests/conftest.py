import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.connection import get_db
from app.db.models.models import Base, User
from app.core.security import get_password_hash
from app.core.config import CONFIG

# Use separate PostgreSQL database for testing
TEST_DATABASE_URL = f"postgresql+asyncpg://{CONFIG.POSTGRES_TEST_USER}:{CONFIG.POSTGRES_TEST_PASSWORD}@localhost:5433/{CONFIG.POSTGRES_TEST_DB}"

engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 
    # async with engine.begin() as conn:
    #   await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    connection = await engine.connect()
    transaction = await connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()

@pytest_asyncio.fixture(autouse=True)
async def override_db_dep(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# --- Data Fixtures ---

@pytest_asyncio.fixture
async def test_user(db_session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("Test1234"),
        role="user",
        is_active=True
    )
    db_session.add(user)
    await db_session.flush()
    return user

@pytest_asyncio.fixture
async def admin_user(db_session):
    admin = User(
        username="adminuser",
        email="admin@example.com",
        hashed_password=get_password_hash("Admin1234"),
        role="admin",
        is_active=True
    )
    db_session.add(admin)
    await db_session.flush()
    return admin

@pytest_asyncio.fixture
async def user_token(client, test_user):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "Test1234"}
    )
    return response.json()["access_token"]

@pytest_asyncio.fixture
async def admin_token(client, admin_user):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "adminuser", "password": "Admin1234"}
    )
    return response.json()["access_token"]