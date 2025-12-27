import pytest
from httpx import AsyncClient
from sqlalchemy import select
from app.db.models.models import User


@pytest.mark.asyncio
async def test_delete_user_with_correct_password(
    client: AsyncClient, test_user, user_token, db_session
):
    """Test successful account deletion with correct password"""
    response = await client.request(
        "DELETE",
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "password": "Test1234",
        },
    )
    assert response.status_code == 204

    # Verify user is deleted from database
    result = await db_session.execute(select(User).filter_by(username="testuser"))
    deleted_user = result.scalar_one_or_none()
    assert deleted_user is None


@pytest.mark.asyncio
async def test_delete_user_with_incorrect_password(
    client: AsyncClient, test_user, user_token, db_session
):
    """Test account deletion fails with incorrect password"""
    response = await client.request(
        "DELETE",
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "password": "WrongPassword123",
        },
    )
    assert response.status_code == 401

    # Verify user still exists in database
    result = await db_session.execute(select(User).filter_by(username="testuser"))
    user = result.scalar_one_or_none()
    assert user is not None


@pytest.mark.asyncio
async def test_delete_user_with_confirmation_text(
    client: AsyncClient, test_user, user_token, db_session
):
    """Test successful account deletion with password and confirmation text"""
    response = await client.request(
        "DELETE",
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"password": "Test1234", "confirm_text": "DELETE MY ACCOUNT"},
    )
    assert response.status_code == 204

    # Verify user is deleted
    result = await db_session.execute(select(User).filter_by(username="testuser"))
    deleted_user = result.scalar_one_or_none()
    assert deleted_user is None


@pytest.mark.asyncio
async def test_delete_user_with_wrong_confirmation_text(
    client: AsyncClient, test_user, user_token, db_session
):
    """Test account deletion fails with wrong confirmation text"""
    response = await client.request(
        "DELETE",
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "password": "Test1234",
            "confirm_text": "delete my account",  # Wrong case
        },
    )
    assert response.status_code == 400

    # Verify user still exists
    result = await db_session.execute(select(User).filter_by(username="testuser"))
    user = result.scalar_one_or_none()
    assert user is not None


@pytest.mark.asyncio
async def test_delete_user_without_authentication(
    client: AsyncClient, test_user, db_session
):
    """Test account deletion fails without authentication"""
    response = await client.request(
        "DELETE",
        "/api/v1/users/me",
        json={
            "password": "Test1234",
        },
    )
    assert response.status_code == 401

    # Verify user still exists
    result = await db_session.execute(select(User).filter_by(username="testuser"))
    user = result.scalar_one_or_none()
    assert user is not None


@pytest.mark.asyncio
async def test_delete_user_without_password(
    client: AsyncClient, test_user, user_token, db_session
):
    """Test account deletion fails without password"""
    response = await client.request(
        "DELETE",
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json={},
    )
    assert response.status_code == 422  # Validation error

    # Verify user still exists
    result = await db_session.execute(select(User).filter_by(username="testuser"))
    user = result.scalar_one_or_none()
    assert user is not None


@pytest.mark.asyncio
async def test_delete_user_with_empty_password(
    client: AsyncClient, test_user, user_token, db_session
):
    """Test account deletion fails with empty password"""
    response = await client.request(
        "DELETE",
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "password": "",
        },
    )
    assert response.status_code == 401

    # Verify user still exists
    result = await db_session.execute(select(User).filter_by(username="testuser"))
    user = result.scalar_one_or_none()
    assert user is not None


@pytest.mark.asyncio
async def test_multiple_users_deletion_isolation(
    client: AsyncClient, test_user, admin_user, user_token, db_session
):
    """Test that deleting one user doesn't affect other users"""
    # Delete test user
    response = await client.request(
        "DELETE",
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "password": "Test1234",
        },
    )
    assert response.status_code == 204

    # Verify test user is deleted
    result = await db_session.execute(select(User).filter_by(username="testuser"))
    deleted_user = result.scalar_one_or_none()
    assert deleted_user is None

    # Verify admin user still exists
    result = await db_session.execute(select(User).filter_by(username="adminuser"))
    admin = result.scalar_one_or_none()
    assert admin is not None
