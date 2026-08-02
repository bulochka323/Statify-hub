import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramConflictError
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


# ----------------------------------------------------
# 🌐 Обробник Callback від Spotify
# ----------------------------------------------------
async def spotify_callback_handler(request):
    """Приймає code від Spotify після входу користувача."""
    code = request.query.get("code")
    error = request.query.get("error")

    if error:
        logger.error(f"Spotify authorization error: {error}")
        return web.Response(
            text="<h2>❌ Помилка авторизації Spotify</h2><p>Будь ласка, поверніться в Telegram та спробуйте ще раз.</p>",
            content_type="text/html",
            status=400
        )

    if code:
        logger.info("Successfully received authorization code from Spotify!")
        html_response = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Statify Hub - Авторизація</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding-top: 50px; background-color: #121212; color: #fff; }
                .card { background: #1e1e1e; display: inline-block; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
                h1 { color: #1DB954; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>✅ Успішна авторизація!</h1>
                <p>Акаунт Spotify підключено. Тепер ви можете закрити цю вкладку та повернутися до бота в Telegram.</p>
            </div>
        </body>
        </html>
        """
        return web.Response(text=html_response, content_type="text/html", status=200)

    return web.Response(text="Missing code parameter", status=400)


async def health_check(request):
    """Хелсчек для Render."""
    return web.Response(text="Statify Hub is running!")


def setup_web_app():
    """Створення та налаштування aiohttp додатка."""
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/callback", spotify_callback_handler)
    return app


# ----------------------------------------------------
# 🚀 Основний запуск
# ----------------------------------------------------
async def main():
    """Основна функція запуску боту та веб-сервера."""

    # Ініціалізація БД
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized!")

    # Створення бота
    bot = Bot(token=settings.bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Middleware для бази даних
    @dp.update.outer_middleware()
    async def db_session_middleware(handler, event, data):
        async for session in get_session():
            data["session"] = session
            return await handler(event, data)

    # Middleware для логування
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    # Маршрути бота
    dp.include_routers(user_router, menu_router)

    # Запуск планувальника
    logger.info("Starting scheduler...")
    spotify_scheduler.start()

    # 🌐 Запуск веб-сервера точно на порті від Render
    web_app = setup_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    
    port = int(os.getenv("PORT", 10000))
    host = "0.0.0.0"
    
    server_started = False
    for attempt in range(1, 6):
        try:
            # Створюємо новий TCPSite на кожну спробу, щоб уникнути RuntimeError
            site = web.TCPSite(runner, host, port)
            await site.start()
            logger.info(f"Web server successfully started on {host}:{port}")
            server_started = True
            break
        except OSError as e:
            if e.errno == 98:  # Address already in use
                logger.warning(f"Port {port} is in use, retrying in 2 seconds... (attempt {attempt}/5)")
                await asyncio.sleep(2)
            else:
                raise e

    if not server_started:
        logger.error(f"Could not bind web server to port {port} after 5 attempts!")

    # Скидання підключень Telegram перед стартом
    logger.info("Clearing webhook and drop pending updates...")
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.sleep(1)

    # Запуск polling з обробкою TelegramConflictError
    logger.info("Bot started!")
    retry_count = 0
    max_retries = 5

    while retry_count < max_retries:
        try:
            await dp.start_polling(bot)
            break
        except TelegramConflictError:
            retry_count += 1
            logger.warning(
                f"Telegram Conflict Error (instance already running). Retrying in 5 seconds... ({retry_count}/{max_retries})"
            )
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Bot error: {e}")
            break
        finally:
            if retry_count >= max_retries:
                logger.error("Max retries reached due to Telegram Conflict. Stopping bot.")

    # Закриття ресурсів
    await runner.cleanup()
    await close_db()
    await spotify_scheduler.shutdown()
    await bot.session.close()
    logger.info("Bot stopped!")


if __name__ == "__main__":
    asyncio.run(main())