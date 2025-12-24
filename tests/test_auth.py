import pytest
from httpx import AsyncClient
from sqlalchemy import select
from app.db.models.models import User

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, db_session):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "Test1234"
        }
    )
    assert response.status_code == 201
    result = await db_session.execute(select(User).filter_by(username="newuser"))
    db_user = result.scalar_one_or_none()
    assert db_user is not None
    assert db_user.email == "new@example.com"

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, test_user):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "Test1234"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, user_token, test_user):
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == test_user.username