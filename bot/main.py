import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ----------------------------------------------------
# 📁 Імпорт ваших модулів проєкту
# ----------------------------------------------------
# Імпортуємо БД та Сервіси
try:
    from db import init_db
except ImportError:
    init_db = None

try:
    from spotify_service import spotify_service
except ImportError:
    spotify_service = None

# Імпортуємо всі Router (хендлери) проєкту
from handlers import router as main_router
from menu_handlers import router as menu_router
from user_handlers import router as user_router

# ----------------------------------------------------
# 📝 Налаштування логування
# ----------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("statify_hub")

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

# Реєструємо роутери зі своїх файлів у Диспетчер
dp.include_router(main_router)
dp.include_router(menu_router)
dp.include_router(user_router)

# ----------------------------------------------------
# 🌐 Web Server & Spotify Callback
# ----------------------------------------------------
async def health_check(request):
    """Health check для Render"""
    return web.Response(text="Statify Hub is running!", status=200)

async def spotify_callback_handler(request):
    """Обробник Callback від Spotify Auth"""
    code = request.rel_url.query.get("code")
    error = request.rel_url.query.get("error")
    state = request.rel_url.query.get("state")  # Повинен містити user_id

    if error:
        logger.error(f"Spotify auth error: {error}")
        return web.Response(text="<h2>❌ Помилка авторизації Spotify</h2>", content_type="text/html", status=400)

    if code and state:
        try:
            user_id = int(state)
            bot_instance: Bot = request.app["bot"]

            # Обмін коду на токен через свій spotify_service (якщо є)
            if spotify_service:
                await spotify_service.finish_auth(user_id=user_id, code=code)

            # Надсилаємо сповіщення в Telegram користувачу
            await bot_instance.send_message(
                chat_id=user_id,
                text="🎉 <b>Акаунт Spotify успішно підключено!</b>\n\nТепер тобі доступні всі функції проєкту.",
            )
            logger.info(f"Spotify authenticated for user {user_id}")

            html_response = """
            <!DOCTYPE html>
            <html>
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
# 🚀 Головна функція запуску (Main)
# ----------------------------------------------------
async def main():
    logger.info("Initializing database...")
    if init_db:
        await init_db()
    logger.info("Database initialized!")

    logger.info("Starting scheduler...")
    scheduler = AsyncIOScheduler()
    scheduler.start()

    # Запускаємо HTTP сервер на порту Render
    web_app = setup_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Web server started on port {PORT}")

    # Скидаємо старі вебхуки та запускаємо polling
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())