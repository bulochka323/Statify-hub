from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from database.models import User, Track, UserTrackHistory, Artist, UserArtistStats, Genre, UserGenreStats
from config.logger import logger
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


class UserRepository:
    """Репозиторій користувачів."""
    
    @staticmethod
    async def create_or_update_user(
        session: AsyncSession,
        telegram_id: int,
        **kwargs
    ) -> User:
        """Створити або оновити користувача."""
        try:
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                user.updated_at = datetime.utcnow()
            else:
                user = User(telegram_id=telegram_id, **kwargs)
                session.add(user)
            
            await session.commit()
            return user
        except Exception as e:
            logger.error(f"Error creating/updating user: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_user(session: AsyncSession, telegram_id: int) -> Optional[User]:
        """Отримати користувача."""
        try:
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    @staticmethod
    async def get_user_by_spotify_id(session: AsyncSession, spotify_id: str) -> Optional[User]:
        """Отримати користувача за Spotify ID."""
        try:
            stmt = select(User).where(User.spotify_id == spotify_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user by spotify id: {e}")
            return None
    
    @staticmethod
    async def get_all_users(session: AsyncSession) -> List[User]:
        """Отримати всіх користувачів."""
        try:
            stmt = select(User).where(User.is_active == True)
            result = await session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []


class TrackRepository:
    """Репозиторій треків."""
    
    @staticmethod
    async def create_or_get_track(
        session: AsyncSession,
        spotify_id: str,
        **kwargs
    ) -> Track:
        """Створити або отримати трек."""
        try:
            stmt = select(Track).where(Track.spotify_id == spotify_id)
            result = await session.execute(stmt)
            track = result.scalar_one_or_none()
            
            if not track:
                track = Track(spotify_id=spotify_id, **kwargs)
                session.add(track)
                await session.commit()
            
            return track
        except Exception as e:
            logger.error(f"Error creating/getting track: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_track(session: AsyncSession, spotify_id: str) -> Optional[Track]:
        """Отримати трек."""
        try:
            stmt = select(Track).where(Track.spotify_id == spotify_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting track: {e}")
            return None


class UserTrackHistoryRepository:
    """Репозиторій історії прослуховування."""
    
    @staticmethod
    async def add_or_update_play(
        session: AsyncSession,
        user_id: int,
        track_spotify_id: str,
        duration_ms: int
    ) -> UserTrackHistory:
        """Додати або оновити прослуховування."""
        try:
            stmt = select(UserTrackHistory).where(
                (UserTrackHistory.user_id == user_id) &
                (UserTrackHistory.track_spotify_id == track_spotify_id)
            )
            result = await session.execute(stmt)
            history = result.scalar_one_or_none()
            
            if history:
                history.play_count += 1
                history.total_time_ms += duration_ms
                history.last_played = datetime.utcnow()
            else:
                history = UserTrackHistory(
                    user_id=user_id,
                    track_spotify_id=track_spotify_id,
                    play_count=1,
                    total_time_ms=duration_ms
                )
                session.add(history)
            
            await session.commit()
            return history
        except Exception as e:
            logger.error(f"Error adding/updating play: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_top_tracks(
        session: AsyncSession,
        user_id: int,
        limit: int = 10,
        days: Optional[int] = None
    ) -> List[UserTrackHistory]:
        """Отримати топ треків."""
        try:
            stmt = select(UserTrackHistory).where(UserTrackHistory.user_id == user_id)
            
            if days:
                date_from = datetime.utcnow() - timedelta(days=days)
                stmt = stmt.where(UserTrackHistory.last_played >= date_from)
            
            stmt = stmt.order_by(desc(UserTrackHistory.play_count)).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting top tracks: {e}")
            return []
    
    @staticmethod
    async def get_total_listening_time(
        session: AsyncSession,
        user_id: int,
        days: Optional[int] = None
    ) -> int:
        """Отримати загальний час прослуховування (в мс)."""
        try:
            stmt = select(UserTrackHistory).where(UserTrackHistory.user_id == user_id)
            
            if days:
                date_from = datetime.utcnow() - timedelta(days=days)
                stmt = stmt.where(UserTrackHistory.last_played >= date_from)
            
            result = await session.execute(stmt)
            histories = result.scalars().all()
            
            return sum(h.total_time_ms for h in histories)
        except Exception as e:
            logger.error(f"Error getting total listening time: {e}")
            return 0


class ArtistRepository:
    """Репозиторій артистів."""
    
    @staticmethod
    async def create_or_get_artist(
        session: AsyncSession,
        spotify_id: str,
        **kwargs
    ) -> Artist:
        """Створити або отримати артиста."""
        try:
            stmt = select(Artist).where(Artist.spotify_id == spotify_id)
            result = await session.execute(stmt)
            artist = result.scalar_one_or_none()
            
            if not artist:
                artist = Artist(spotify_id=spotify_id, **kwargs)
                session.add(artist)
                await session.commit()
            
            return artist
        except Exception as e:
            logger.error(f"Error creating/getting artist: {e}")
            await session.rollback()
            raise


class UserArtistStatsRepository:
    """Репозиторій статистики артистів."""
    
    @staticmethod
    async def add_or_update_play(
        session: AsyncSession,
        user_id: int,
        artist_spotify_id: str,
        duration_ms: int
    ) -> UserArtistStats:
        """Додати або оновити прослуховування артиста."""
        try:
            stmt = select(UserArtistStats).where(
                (UserArtistStats.user_id == user_id) &
                (UserArtistStats.artist_spotify_id == artist_spotify_id)
            )
            result = await session.execute(stmt)
            stats = result.scalar_one_or_none()
            
            if stats:
                stats.play_count += 1
                stats.total_time_ms += duration_ms
                stats.last_played = datetime.utcnow()
            else:
                stats = UserArtistStats(
                    user_id=user_id,
                    artist_spotify_id=artist_spotify_id,
                    play_count=1,
                    total_time_ms=duration_ms
                )
                session.add(stats)
            
            await session.commit()
            return stats
        except Exception as e:
            logger.error(f"Error adding/updating artist play: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_top_artists(
        session: AsyncSession,
        user_id: int,
        limit: int = 10,
        days: Optional[int] = None
    ) -> List[UserArtistStats]:
        """Отримати топ артистів."""
        try:
            stmt = select(UserArtistStats).where(UserArtistStats.user_id == user_id)
            
            if days:
                date_from = datetime.utcnow() - timedelta(days=days)
                stmt = stmt.where(UserArtistStats.last_played >= date_from)
            
            stmt = stmt.order_by(desc(UserArtistStats.play_count)).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting top artists: {e}")
            return []
