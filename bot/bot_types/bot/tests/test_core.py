"""
Приклади тестів для бота.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from database.repository import UserRepository
from services.spotify_service import UserService
from spotify.spotify_api import SpotifyAPI


@pytest.fixture
async def mock_session():
    """Mock асинхронної сесії."""
    return AsyncMock(spec=AsyncSession)


@pytest.mark.asyncio
async def test_create_user(mock_session):
    """Тест створення користувача."""
    user_repo = UserRepository()
    
    user = await user_repo.create_or_update_user(
        mock_session,
        telegram_id=123456789,
        display_name="Test User"
    )
    
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_user(mock_session):
    """Тест отримання користувача."""
    mock_user = User(
        id=1,
        telegram_id=123456789,
        display_name="Test User",
        level=1,
        xp=0
    )
    
    mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
    
    user_repo = UserRepository()
    user = await user_repo.get_user(mock_session, 123456789)
    
    assert user.telegram_id == 123456789


@pytest.mark.asyncio
async def test_spotify_auth_url():
    """Тест генерації URL авторизації Spotify."""
    spotify = SpotifyAPI()
    auth_url = spotify.get_authorize_url()
    
    assert "https://accounts.spotify.com/authorize" in auth_url
    assert "client_id=" in auth_url
    assert "scope=" in auth_url


@pytest.mark.asyncio
async def test_user_service_add_xp(mock_session):
    """Тест додавання XP."""
    mock_user = User(
        id=1,
        telegram_id=123456789,
        display_name="Test User",
        level=1,
        xp=0
    )
    
    mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
    
    user_service = UserService(mock_session)
    user = await user_service.add_xp(123456789, 100)
    
    assert user.xp == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
