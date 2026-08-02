import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.logger import setup_logging
from config.settings import settings
from database.db import close_db, get_session, init_db
from handlers.menu_handlers import router as menu_router
from handlers.user_handlers import router as user_router
from middlewares.logging_middleware import LoggingMiddleware
from scheduler.tasks import spotify_scheduler

# Налаштування логування
setup_logging()
logger = logging.getLogger(__name__)


async def main():
    """Основна функція запуску боту."""

    # Ініціалізація БД
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized!")

    # Створення бота
    bot = Bot(token=settings.bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Додавання middleware для бази даних (автоматично передає 'session' у хендлери)
    @dp.update.outer_middleware()
    async def db_session_middleware(handler, event, data):
        async for session in get_session():
            data["session"] = session
            return await handler(event, data)

    # Додавання middleware для логування
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    # Додавання маршрутів
    dp.include_routers(user_router, menu_router)

    # Запуск планувальника
    logger.info("Starting scheduler...")
    spotify_scheduler.start()

    # Запуск polling
    logger.info("Bot started!")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        # Закриття БД та планувальника
        await close_db()
        await spotify_scheduler.shutdown()
        await bot.session.close()
        logger.info("Bot stopped!")


if __name__ == "__main__":
    asyncio.run(main())