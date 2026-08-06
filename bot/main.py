import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ----------------------------------------------------
# 📝 Налаштування логування
# ----------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("statify_hub")

# ----------------------------------------------------
# 📂 Імпорт бази даних (з імпортом async_session)
# ----------------------------------------------------
init_db = None
close_db = None
async_session = None

try:
    from db import init_db, close_db, async_session
except ImportError:
    try:
        from bot.db import init_db, close_db, async_session
    except ImportError:
        logger.error("❌ Не вдалося знайти файл db.py!")

try:
    from spotify_service import spotify_service
except ImportError:
    try:
        from bot.spotify_service import spotify_service
    except ImportError:
        spotify_service = None

# ----------------------------------------------------
# 🛠 Middleware для автоматичного створення сесії БД
# ----------------------------------------------------
class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if not self.session_pool:
            logger.error("DbSessionMiddleware: session_pool is None!")
            data["session"] = None
            return await handler(event, data)

        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)

# ----------------------------------------------------
# 📂 Імпорт роутерів проєкту
# ----------------------------------------------------
routers_to_include = []

try:
    from handlers.menu_handlers import router as menu_router
    routers_to_include.append(menu_router)
except ImportError:
    try:
        from menu_handlers import router as menu_router
        routers_to_include.append(menu_router)
    except ImportError:
        logger.warning("menu_handlers.py не знайдено")

try:
    from handlers.user_handlers import router as user_router
    routers_to_include.append(user_router)
except ImportError:
    try:
        from user_handlers import router as user_router
        routers_to_include.append(user_router)
    except ImportError:
        logger.warning("user_handlers.py не знайдено")

# ----------------------------------------------------
# 🔐 Змінні середовища
# ----------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8080))

# ----------------------------------------------------
# 🤖 Ініціалізація Бота та Диспетчера
# ----------------------------------------------------
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# РЕЄСТРУЄМО МІДЛВАРЬ З ТВОЇМ async_session
if async_session:
    dp.update.outer_middleware(DbSessionMiddleware(async_session))
    logger.info("DbSessionMiddleware успішно підключено з async_session!")
else:
    logger.error("⚠️ async_session не знайдено, Middleware НЕ підключено!")

# Підключаємо роутери
for r in routers_to_include:
    dp.include_router(r)

# ----------------------------------------------------
# 🌐 Web Server & Spotify Callback
# ----------------------------------------------------
async def health_check(request):
    return web.Response(text="Statify Hub is running!", status=200)

async def spotify_callback_handler(request):
    code = request.rel_url.query.get("code")
    error = request.rel_url.query.get("error")
    state = request.rel_url.query.get("state")

    if error:
        logger.error(f"Spotify auth error: {error}")
        return web.Response(text="<h2>❌ Помилка авторизації Spotify</h2>", content_type="text/html", status=400)

    if code and state:
        try:
            user_id = int(state)
            bot_instance: Bot = request.app["bot"]

            if spotify_service and hasattr(spotify_service, "finish_auth"):
                await spotify_service.finish_auth(user_id=user_id, code=code)

            await bot_instance.send_message(
                chat_id=user_id,
                text="🎉 <b>Акаунт Spotify успішно підключено!</b>\n\nТепер вам доступні всі функції бота.",
            )
            logger.info(f"Spotify connected for user {user_id}")

            html_response = """
            <!DOCTYPE html>
            <html lang="uk">
            <head><meta charset="utf-8"><title>Statify Hub</title></head>
            <body style="background:#121212;color:#1DB954;text-align:center;padding-top:100px;font-family:sans-serif;">
                <h1>✅ Успішна авторизація!</h1>
                <p style="color:#fff;">Можете закрити це вікно та повернутися до бота в Telegram.</p>
            </body>
            </html>
            """
            return web.Response(text=html_response, content_type="text/html", status=200)

        except Exception as e:
            logger.error(f"Error handling spotify callback: {e}")
            return web.Response(text="<h2>❌ Помилка обробки токена</h2>", content_type="text/html", status=500)

    return web.Response(text="Missing code or state parameter", status=400)

def setup_web_app():
    app = web.Application()
    app["bot"] = bot
    app.router.add_get("/", health_check)
    app.router.add_get("/callback", spotify_callback_handler)
    return app

# ----------------------------------------------------
# 🚀 Точка входу
# ----------------------------------------------------
async def main():
    logger.info("Initializing database...")
    if init_db:
        try:
            await init_db()
            logger.info("Database initialized successfully!")
        except Exception as db_err:
            logger.error(f"Database init error: {db_err}")

    logger.info("Starting scheduler...")
    scheduler = AsyncIOScheduler()
    scheduler.start()

    web_app = setup_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Web server started on port {PORT}")

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()
        if close_db:
            await close_db()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())