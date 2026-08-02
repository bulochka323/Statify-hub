from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from config.logger import logger
from database.repository import (
    ArtistRepository,
    TrackRepository,
    UserArtistStatsRepository,
    UserRepository,
    UserTrackHistoryRepository,
)
from spotify.spotify_api import SpotifyAPI


class UserService:
    """Сервіс для роботи з користувачами."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository()
        self.spotify = SpotifyAPI()

    async def register_user(self, telegram_id: int, display_name: str) -> Any:
        """Зареєструвати користувача."""
        return await self.user_repo.create_or_update_user(
            self.session,
            telegram_id=telegram_id,
            display_name=display_name
        )

    async def update_user(self, telegram_id: int, **kwargs) -> Any:
        """Оновити довільні дані користувача (наприклад, мову чи налаштування)."""
        return await self.user_repo.create_or_update_user(
            self.session,
            telegram_id=telegram_id,
            **kwargs
        )

    async def link_spotify(
        self,
        telegram_id: int,
        spotify_id: str,
        access_token: str,
        refresh_token: str,
        display_name: str,
        profile_image_url: Optional[str] = None
    ) -> Any:
        """Привʼязати Spotify акаунт."""
        return await self.user_repo.create_or_update_user(
            self.session,
            telegram_id=telegram_id,
            spotify_id=spotify_id,
            spotify_access_token=access_token,
            spotify_refresh_token=refresh_token,
            display_name=display_name,
            profile_image_url=profile_image_url
        )

    async def get_user(self, telegram_id: int) -> Optional[Any]:
        """Отримати користувача."""
        return await self.user_repo.get_user(self.session, telegram_id)

    async def add_xp(self, telegram_id: int, xp: int) -> Any:
        """Додати XP користувачу."""
        user = await self.get_user(telegram_id)
        if user:
            user.xp += xp
            # Простий розрахунок рівня
            user.level = (user.xp // 1000) + 1
            await self.session.commit()
        return user


class SpotifyService:
    """Сервіс для роботи зі Spotify."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.spotify = SpotifyAPI()
        self.track_repo = TrackRepository()
        self.history_repo = UserTrackHistoryRepository()
        self.artist_repo = ArtistRepository()
        self.artist_stats_repo = UserArtistStatsRepository()

    async def sync_recently_played(
        self,
        user_id: int,
        access_token: str,
        limit: int = 50
    ) -> bool:
        """Синхронізувати недавно прослухані треки."""
        try:
            data = await self.spotify.get_recently_played(access_token, limit)
            if not data or "items" not in data:
                return False

            for item in data["items"]:
                track_data = item.get("track", {})
                if not track_data:
                    continue

                # Зберегти трек
                track = await self.track_repo.create_or_get_track(
                    self.session,
                    spotify_id=track_data["id"],
                    name=track_data.get("name", "Unknown"),
                    artist=", ".join([a["name"] for a in track_data.get("artists", [])]),
                    album=track_data.get("album", {}).get("name", "Unknown"),
                    duration_ms=track_data.get("duration_ms", 0),
                    image_url=track_data.get("album", {}).get("images", [{}])[0].get("url"),
                    spotify_url=track_data.get("external_urls", {}).get("spotify")
                )

                # Зберегти історію
                await self.history_repo.add_or_update_play(
                    self.session,
                    user_id,
                    track_data["id"],
                    track_data.get("duration_ms", 0)
                )

                # Зберегти артистів
                for artist_data in track_data.get("artists", []):
                    artist = await self.artist_repo.create_or_get_artist(
                        self.session,
                        spotify_id=artist_data["id"],
                        name=artist_data.get("name", "Unknown"),
                        spotify_url=artist_data.get("external_urls", {}).get("spotify")
                    )

                    await self.artist_stats_repo.add_or_update_play(
                        self.session,
                        user_id,
                        artist_data["id"],
                        track_data.get("duration_ms", 0)
                    )

            return True
        except Exception as e:
            logger.error(f"Error syncing recently played: {e}")
            return False

    async def get_currently_playing_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Отримати інформацію про трек, що зараз грає."""
        try:
            data = await self.spotify.get_currently_playing(access_token)
            if not data or not data.get("item"):
                return None

            item = data["item"]
            return {
                "name": item.get("name"),
                "artist": ", ".join([a["name"] for a in item.get("artists", [])]),
                "album": item.get("album", {}).get("name"),
                "image": item.get("album", {}).get("images", [{}])[0].get("url"),
                "url": item.get("external_urls", {}).get("spotify"),
                "is_playing": data.get("is_playing", False),
                "duration_ms": item.get("duration_ms", 0),
                "progress_ms": data.get("progress_ms", 0),
            }
        except Exception as e:
            logger.error(f"Error getting currently playing: {e}")
            return None

    async def get_top_items(
        self,
        access_token: str,
        item_type: str = "artists",
        limit: int = 10,
        time_range: str = "medium_term"
    ) -> Optional[List[Dict[str, Any]]]:
        """Отримати топ артистів або треків."""
        try:
            data = await self.spotify.get_top_items(access_token, item_type, limit, time_range)
            if not data or "items" not in data:
                return None

            result = []
            for item in data["items"]:
                result.append({
                    "name": item.get("name"),
                    "image": item.get("images", [{}])[0].get("url") if item.get("images") else None,
                    "url": item.get("external_urls", {}).get("spotify"),
                    "id": item.get("id"),
                })

            return result
        except Exception as e:
            logger.error(f"Error getting top items: {e}")
            return None