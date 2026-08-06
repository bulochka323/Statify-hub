import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ----------------------------------------------------
# 📝 Налаштування логування
# ----------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("statify_hub")

# ----------------------------------------------------
# 🔐 Змінні середовища (Environment Variables)
# ----------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")  # Наприклад: https://statify-hub.onrender.com/callback
PORT = int(os.getenv("PORT", 8080))

SPOTIFY_SCOPES = "user-read-recently-played user-top-read user-read-currently-playing"

# Fake In-Memory DB / Заглушка для БД (заміни на свою роботу з SQLite/PostgreSQL)
USER_TOKENS = {}

# ----------------------------------------------------
# 🎵 Допоміжні функції Spotify OAuth
# ----------------------------------------------------
def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPES
    )

def get_auth_url(user_id: int) -> str:
    sp_oauth = get_spotify_oauth()
    # Передаємо user_id у параметр state, щоб під час callback впізнати юзера
    return sp_oauth.get_authorize_url(state=str(user_id))

# ----------------------------------------------------
# 🤖 Ініціалізація Telegram Бота та Диспетчера
# ----------------------------------------------------
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# ----------------------------------------------------
# 🔘 Клавіатури та Меню
# ----------------------------------------------------
def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎵 Щораз грає зараз", callback_data="currently_playing"),
            InlineKeyboardButton(text="📜 Нещодавні треки", callback_data="recently_played")
        ],
        [
            InlineKeyboardButton(text="📊 Топ треки", callback_data="top_tracks"),
            InlineKeyboardButton(text="👨‍🎤 Топ виконавці", callback_data="top_artists")
        ],
        [
            InlineKeyboardButton(text="⚙️ Налаштування", callback_data="settings")
        ]
    ])
    return keyboard

# ----------------------------------------------------
# 📥 Хендлери команд Telegram
# ----------------------------------------------------
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    
    # Перевіряємо, чи авторизований користувач
    if user_id in USER_TOKENS:
        await message.answer(
            f"Вітаю знову, <b>{message.from_user.first_name}</b>! 👋\n\nОбери потрібний розділ нижче:",
            reply_markup=get_main_menu()
        )
    else:
        auth_url = get_auth_url(user_id)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Авторизуватися в Spotify", url=auth_url)]
        ])
        await message.answer(
            f"Привіт, <b>{message.from_user.first_name}</b>! 🎧\n\n"
            "Щоб використовувати <b>Statify Hub</b> та отримувати свою статистику, авторизуйся через Spotify за посиланням нижче:",
            reply_markup=keyboard
        )

# Callback-хендлер для кнопок головного меню
@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if user_id not in USER_TOKENS:
        auth_url = get_auth_url(user_id)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Авторизуватися в Spotify", url=auth_url)]
        ])
        await callback_query.message.answer(
            "❌ Ви не авторизовані! Будь ласка, підключіть ваш акаунт Spotify:",
            reply_markup=keyboard
        )
        await callback_query.answer()
        return

    tokens = USER_TOKENS[user_id]
    sp = spotipy.Spotify(auth=tokens["access_token"])

    if data == "currently_playing":
        try:
            current = sp.current_user_playing_track()
            if current and current.get("is_playing"):
                track_name = current["item"]["name"]
                artist_name = current["item"]["artists"][0]["name"]
                await callback_query.message.answer(f"🎶 зараз грає: <b>{artist_name} — {track_name}</b>")
            else:
                await callback_query.message.answer("⏸ Наразі нічого не відтворюється.")
        except Exception as e:
            logger.error(f"Error fetching current playing track: {e}")
            await callback_query.message.answer("❌ Помилка отримання даних від Spotify.")

    elif data == "recently_played":
        try:
            recent = sp.current_user_recently_played(limit=5)
            text = "📜 <b>Останні 5 треків:</b>\n\n"
            for idx, item in enumerate(recent["items"], 1):
                track = item["track"]
                text += f"{idx}. {track['artists'][0]['name']} — {track['name']}\n"
            await callback_query.message.answer(text)
        except Exception as e:
            logger.error(f"Error fetching recently played: {e}")
            await callback_query.message.answer("❌ Помилка отримання даних від Spotify.")

    elif data == "top_tracks":
        try:
            top = sp.current_user_top_tracks(limit=5, time_range="short_term")
            text = "🔥 <b>Твій Топ-5 треків за місяць:</b>\n\n"
            for idx, track in enumerate(top["items"], 1):
                text += f"{idx}. {track['artists'][0]['name']} — {track['name']}\n"
            await callback_query.message.answer(text)
        except Exception as e:
            logger.error(f"Error fetching top tracks: {e}")
            await callback_query.message.answer("❌ Помилка отримання даних від Spotify.")

    elif data == "top_artists":
        try:
            top = sp.current_user_top_artists(limit=5, time_range="short_term")
            text = "👨‍🎤 <b>Твій Топ-5 виконавців за місяць:</b>\n\n"
            for idx, artist in enumerate(top["items"], 1):
                text += f"{idx}. {artist['name']}\n"
            await callback_query.message.answer(text)
        except Exception as e:
            logger.error(f"Error fetching top artists: {e}")
            await callback_query.message.answer("❌ Помилка отримання даних від Spotify.")

    elif data == "settings":
        await callback_query.message.answer("⚙️ Налаштування знаходяться в розробці.")

    await callback_query.answer()

# ----------------------------------------------------
# 🌐 Обробники HTTP Веб-Сервера aiohttp
# ----------------------------------------------------
async def health_check(request):
    """Health-check ендпоінт для Render"""
    return web.Response(text="Statify Hub is alive!", status=200)

async def spotify_callback_handler(request):
    """Приймає code від Spotify, обмінює його на токени та надсилає меню в Telegram."""
    code = request.rel_url.query.get("code")
    error = request.rel_url.query.get("error")
    state = request.rel_url.query.get("state")  # Сюди приходить user_id

    if error:
        logger.error(f"Spotify authorization error: {error}")
        return web.Response(text="<h2>❌ Помилка авторизації Spotify</h2>", content_type="text/html", status=400)

    if code and state:
        try:
            user_id = int(state)
            sp_oauth = get_spotify_oauth()
            token_info = sp_oauth.get_access_token(code=code, check_cache=False)

            # Зберігаємо токен (заміни на збереження в DB)
            USER_TOKENS[user_id] = token_info

            # Надсилаємо сповіщення юзеру в Telegram із кнопками меню
            bot_instance: Bot = request.app["bot"]
            await bot_instance.send_message(
                chat_id=user_id,
                text="🎉 <b>Акаунт Spotify успішно підключено!</b>\n\nТепер тобі доступні всі функції бота. Обирай дію з меню нижче:",
                reply_markup=get_main_menu()
            )
            logger.info(f"Successfully authenticated Spotify for user_id={user_id}")

            html_response = """
            <!DOCTYPE html>
            <html lang="uk">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Statify Hub - Авторизація</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #121212;
                        color: #ffffff;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .card {
                        background-color: #181818;
                        padding: 40px;
                        border-radius: 16px;
                        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
                        text-align: center;
                        max-width: 400px;
                    }
                    h1 { color: #1DB954; font-size: 24px; margin-bottom: 16px; }
                    p { color: #b3b3b3; font-size: 16px; line-height: 1.5; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>✅ Успішна авторизація!</h1>
                    <p>Акаунт Spotify підключено. Поверніться до бота в Telegram для продовження.</p>
                </div>
            </body>
            </html>
            """
            return web.Response(text=html_response, content_type="text/html", status=200)

        except Exception as e:
            logger.error(f"Failed to process callback: {e}")
            return web.Response(text="<h2>❌ Помилка обробки токена Spotify</h2>", content_type="text/html", status=500)

    return web.Response(text="Missing code or state parameter", status=400)

def setup_web_app():
    app = web.Application()
    app["bot"] = bot
    app.router.add_get("/", health_check)
    app.router.add_get("/callback", spotify_callback_handler)
    return app

# ----------------------------------------------------
# ⏰ Планувальник задач (APScheduler)
# ----------------------------------------------------
class SpotifyScheduler:
    @staticmethod
    async def sync_all_users():
        logger.info("Scheduler task: Synchronizing all users...")

    @staticmethod
    async def daily_reminder():
        logger.info("Scheduler task: Sending daily reminders...")

    @staticmethod
    async def weekly_stats():
        logger.info("Scheduler task: Generating weekly stats...")

def init_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(SpotifyScheduler.sync_all_users, 'interval', minutes=30, id="SpotifyScheduler.sync_all_users")
    scheduler.add_job(SpotifyScheduler.daily_reminder, 'cron', hour=20, minute=0, id="SpotifyScheduler.daily_reminder")
    scheduler.add_job(SpotifyScheduler.weekly_stats, 'cron', day_of_week='mon', hour=10, minute=0, id="SpotifyScheduler.weekly_stats")
    scheduler.start()
    logger.info("Scheduler started!")

# ----------------------------------------------------
# 🚀 Головна точка входу (Main)
# ----------------------------------------------------
async def main():
    logger.info("Initializing database...")
    # Тут може бути ініціалізація вашої БД (наприклад, init_db())
    logger.info("Database initialized!")

    logger.info("Starting scheduler...")
    init_scheduler()

    # Запуск HTTP веб-сервера aiohttp
    web_app = setup_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"🚀 Web server successfully started on http://0.0.0.0:{PORT}")

    # Очищення вебхуків та запуск бота
    logger.info("Clearing webhook and drop pending updates...")
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Bot started!")
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())