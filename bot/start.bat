@echo off
REM STATIFY HUB - Простий Запуск
REM Цей файл автоматично запустить бота після налаштування

cd /d "%~dp0"

REM Переконатись, що Python встановлено
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не встановлено!
    echo.
    echo Завантажте Python з https://www.python.org/
    echo При встановленні ОБОВ'ЯЗКОВО виберіть "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Перевірити залежності
echo Перевірка залежностей...
pip show aiogram >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📦 Встановлюємо залежності...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Помилка при встановленні залежностей!
        pause
        exit /b 1
    )
)

REM Перевірити .env
if not exist .env (
    echo.
    echo ❌ .env файл не знайдено!
    echo.
    echo Скопіюємо з .env.example...
    if exist .env.example (
        copy .env.example .env
        echo ✅ .env створено!
        echo.
        echo ⚠️  ОБОВ'ЯЗКОВО відредагуйте .env та вставте свої дані:
        echo    - BOT_TOKEN (від @BotFather)
        echo    - SPOTIFY_CLIENT_ID та SPOTIFY_CLIENT_SECRET
        echo.
        echo Файл .env знаходиться в цій папці.
        echo Відкрийте його та вставте дані.
        echo.
        pause
    )
)

REM Запуск тесту налаштувань
echo.
echo 🧪 Перевірка налаштувань...
python test_setup.py
if errorlevel 1 (
    echo.
    echo ⚠️  Деякі перевірки не пройдені!
    echo Виправте помилки та запустіть знову.
    pause
    exit /b 1
)

echo.
echo 🚀 Запуск STATIFY HUB Бота...
echo.

REM Запуск бота
python main.py

if errorlevel 1 (
    echo.
    echo ❌ Помилка при запуску бота!
    pause
)
