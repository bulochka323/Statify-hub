@echo off
REM ======================================================================
REM STATIFY HUB - Автоматична Установка Бота
REM ======================================================================
REM Цей скрипт встановить всі залежності та налаштує бота
REM Вам потрібно тільки вставити дані в .env файл!
REM ======================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   STATIFY HUB BOT - SETUP                      ║
echo ║                  🎵 Spotify Telegram Bot 🎵                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Проверка Python
echo [1/6] Перевірка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не встановлено! Завантажте з https://www.python.org/
    echo    Переконайтесь, що встановлює "Add Python to PATH"
    pause
    exit /b 1
)
echo ✅ Python знайдено!
echo.

REM Проверка та встановлення pip
echo [2/6] Встановлення pip...
python -m pip install --upgrade pip >nul 2>&1
echo ✅ pip оновлено!
echo.

REM Встановлення залежностей
echo [3/6] Встановлення залежностей Python (це займе ~ 2-3 хвилини)...
echo        Встановлюємо: aiogram, sqlalchemy, asyncpg, redis, pillow, aiohttp...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Помилка при встановленні залежностей!
    pause
    exit /b 1
)
echo ✅ Залежності встановлені!
echo.

REM Перевірка та створення .env файлу
echo [4/6] Налаштування конфігурації...
if exist .env (
    echo ⚠️  .env файл вже існує. Пропускаємо...
) else (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ .env файл створено з .env.example
        echo.
        echo ⚠️  ВАЖЛИВО: Відредагуйте .env файл та вставте ваші дані:
        echo    - BOT_TOKEN (від @BotFather в Telegram)
        echo    - SPOTIFY_CLIENT_ID та SPOTIFY_CLIENT_SECRET
        echo    - DATABASE_URL та REDIS_URL (якщо не localhost)
        echo.
    ) else (
        echo ❌ .env.example не знайдено!
        pause
        exit /b 1
    )
)
echo.

REM Створення папок
echo [5/6] Створення необхідних папок...
if not exist logs mkdir logs
if not exist uploads mkdir uploads
if not exist temp mkdir temp
echo ✅ Папки створено!
echo.

REM Перевірка PostgreSQL та Redis
echo [6/6] Перевірка бази даних...
echo.
echo ℹ️  Переконайтесь, що запущені:
echo    📦 PostgreSQL на localhost:5432
echo    📦 Redis на localhost:6379
echo.
echo    Якщо використовуєте Docker:
echo    $ docker-compose up -d
echo.
echo.

REM Запитання про запуск
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ✅ ВСТАНОВЛЕННЯ ЗАВЕРШЕНО!                        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Наступні кроки:
echo.
echo 1️⃣  Відредагуйте .env файл:
echo    notepad .env
echo.
echo 2️⃣  Запустіть PostgreSQL та Redis:
echo    - Локально: запустіть postgres та redis-server
echo    - Docker: docker-compose up -d
echo.
echo 3️⃣  Запустіть бота:
echo    python main.py
echo.
echo 4️⃣  Запустіть його з Docker (альтернатива):
echo    docker-compose up --build
echo.

set /p launch="Запустити бота зараз? (y/n): "
if /i "%launch%"=="y" (
    echo.
    echo 🚀 Запуск бота...
    python main.py
) else (
    echo.
    echo Готово! Запустіть python main.py коли будете готові.
    pause
)

endlocal
