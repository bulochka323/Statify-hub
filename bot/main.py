import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
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
# 📂 Безпечні імпорти модулів проєкту
# ----------------------------------------------------
# БД та додаткові сервіси
try:
    from db import init_db
except ImportError:
    try:
        from bot.db import init_db
    except ImportError:
        init_db = None

try:
    from spotify_service import spotify_service
except ImportError:
    try:
        from bot.spotify_service import spotify_service
    except ImportError:
        spotify_service = None

# Динамічно імпортуємо всі доступні роутери з проєкту
routers_to_include = []

# Імпорт menu_handlers
try:
    from handlers.menu_handlers import router as menu_router
    routers_to_include.append(menu_router)
except ImportError:
    try:
        from menu_handlers import router as menu_router
        routers_to_include.append(menu_router)
    except ImportError:
        logger.warning("menu_handlers.py не знайдено або не містить 'router'")

# Імпорт user_handlers
try:
    from handlers.user_handlers import router as user_router
    routers_to_include.append(user_router)
except ImportError:
    try:
        from user_handlers import router as user_router
        routers_to_include.append(user_router)
    except ImportError:
        logger.warning("user_handlers.py не знайдено або не містить 'router'")

# Імпорт стандартного handlers (якщо існує)
try:
    from handlers import router as base_router
    routers_to_include.append(base_router)
except ImportError:
    try:
        from handlers.handlers import router as base_router
        routers_to_include.append(base_router)
    except ImportError:
        pass

# ----------------------------------------------------
# 🔐 Змінні середовища (Environment Variables)
# ----------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8080))

# ----------------------------------------------------
# 🤖 Ініціалізація Telegram Бота та Диспетчера
# ----------------------------------------------------
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Підключаємо всі знайдені роутери в диспетчер
for r in routers_to_include:
    dp.include_router(r)

# ----------------------------------------------------
# 🌐 Web Server (aiohttp) & Spotify Callback
# ----------------------------------------------------
async def health_check(request):
    """Health check endpoint для Render"""
    return web.Response(text="Statify Hub is running!", status=200)

async def spotify_callback_handler(request):
    """Обробник веб-хука/авторизації від Spotify API"""
    code = request.rel_url.query.get("code")
    error = request.rel_url.query.get("error")
    state = request.rel_url.query.get("state")  # Передається user_id

    if error:
        logger.error(f"Spotify authorization error: {error}")
        return web.Response(text="<h2>❌ Помилка авторизації Spotify</h2>", content_type="text/html", status=400)

    if code and state:
        try:
            user_id = int(state)
            bot_instance: Bot = request.app["bot"]

            # Завершуємо авторизацію через ваш spotify_service
            if spotify_service and hasattr(spotify_service, "finish_auth"):
                await spotify_service.finish_auth(user_id=user_id, code=code)

            # Сповіщаємо користувача в Telegram
            await bot_instance.send_message(
                chat_id=user_id,
                text="🎉 <b>Акаунт Spotify успішно підключено!</b>\n\nТепер вам доступні всі функції бота.",
            )
            logger.info(f"Successfully authenticated Spotify for user_id={user_id}")

            html_response = """
            <!DOCTYPE html>
            <html lang="uk">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Statify Hub</title>
                <style>
                    body {
                        background-color: #121212;
                        color: #1DB954;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .box {
                        background: #181818;
                        padding: 40px;
                        border-radius: 12px;
                        text-align: center;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
                    }
                    h1 { margin-bottom: 10px; }
                    p { color: #b3b3b3; }
                </style>
            </head>
            <body>
                <div class="box">
                    <h1>✅ Успішна авторизація!</h1>
                    <p>Поверніться до Telegram-бота для використання сервісу.</p>
                </div>
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
# 🚀 Головна точка входу (Main)
# ----------------------------------------------------
async def main():
    logger.info("Initializing database...")
    if init_db:
        try:
            await init_db()
            logger.info("Database initialized!")
        except Exception as db_err:
            logger.error(f"Database init error: {db_err}")
    else:
        logger.info("No DB init function detected, skipping...")

    logger.info("Starting scheduler...")
    scheduler = AsyncIOScheduler()
    scheduler.start()

    # Запуск aiohttp сервера для підтримки порту Render
    web_app = setup_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Web server successfully started on port {PORT}")

    # Скидаємо старі вебхуки та запускаємо polling
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot is polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())