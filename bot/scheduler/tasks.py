import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import async_session
from database.repository import UserRepository
from services.spotify_service import SpotifyService
from config.logger import logger


class SpotifyScheduler:
    """Планувальник для синхронізації Spotify даних."""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
    
    async def sync_all_users(self):
        """Синхронізувати всіх активних користувачів."""
        try:
            async with async_session() as session:
                user_repo = UserRepository()
                users = await user_repo.get_all_users(session)
                
                logger.info(f"Syncing {len(users)} users...")
                
                for user in users:
                    if not user.spotify_access_token:
                        continue
                    
                    try:
                        spotify_service = SpotifyService(session)
                        await spotify_service.sync_recently_played(
                            user.id,
                            user.spotify_access_token
                        )
                        
                        user.last_sync = datetime.utcnow()
                        await session.commit()
                    except Exception as e:
                        logger.error(f"Error syncing user {user.id}: {e}")
                        continue
                
                logger.info("Sync completed!")
        
        except Exception as e:
            logger.error(f"Error in sync_all_users: {e}")
    
    async def daily_reminder(self):
        """Щоденне нагадування."""
        try:
            async with async_session() as session:
                user_repo = UserRepository()
                users = await user_repo.get_all_users(session)
                logger.info(f"Daily reminder for {len(users)} users")
        except Exception as e:
            logger.error(f"Error in daily_reminder: {e}")
    
    async def weekly_stats(self):
        """Генерація щотижневої статистики."""
        try:
            logger.info("Generating weekly stats...")
        except Exception as e:
            logger.error(f"Error in weekly_stats: {e}")
    
    def start(self):
        """Запустити планувальник."""
        # Синхронізація кожні 6 годин
        self.scheduler.add_job(
            self.sync_all_users,
            "interval",
            hours=6,
            id="sync_spotify"
        )
        
        # Щоденне нагадування о 9:00
        self.scheduler.add_job(
            self.daily_reminder,
            "cron",
            hour=9,
            minute=0,
            id="daily_reminder"
        )
        
        # Щотижневі статистики у понеділок о 10:00
        self.scheduler.add_job(
            self.weekly_stats,
            "cron",
            day_of_week=0,
            hour=10,
            minute=0,
            id="weekly_stats"
        )
        
        self.scheduler.start()
        logger.info("Scheduler started!")
    
    async def shutdown(self):
        """Зупинити планувальник."""
        self.scheduler.shutdown()
        logger.info("Scheduler shutdown!")


spotify_scheduler = SpotifyScheduler()
