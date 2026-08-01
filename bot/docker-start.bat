@echo off
REM STATIFY HUB - Docker Setup для Windows
REM Цей скрипт встановить та запустить бота в Docker

cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║           STATIFY HUB BOT - DOCKER SETUP (Windows)             ║
echo ║                  🐳 Docker Edition 🐳                          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Перевірка Docker
echo [1/3] Перевірка Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker не встановлено!
    echo.
    echo Завантажте Docker Desktop з https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)
echo ✅ Docker знайдено!
echo.

REM Налаштування .env
echo [2/3] Налаштування конфігурації...
if exist .env (
    echo ⚠️  .env файл вже існує. Пропускаємо...
) else (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ .env файл створено!
        echo.
        echo ⚠️  ВАЖЛИВО: Відредагуйте .env та вставте ваші дані:
        echo    - BOT_TOKEN
        echo    - SPOTIFY_CLIENT_ID та SPOTIFY_CLIENT_SECRET
        echo.
    )
)
echo.

REM Запуск контейнерів
echo [3/3] Запуск Docker контейнерів...
echo.
echo Перевірте, чи відредагували .env файл!
echo Якщо ні, натисніть Ctrl+C і відредагуйте його.
echo.

set /p proceed="Продовжити запуск? (y/n): "
if /i not "%proceed%"=="y" (
    echo.
    echo Відредагуйте .env та запустіть скрипт заново.
    pause
    exit /b 1
)

echo.
echo 🚀 Запуск контейнерів...
docker-compose up -d

if errorlevel 1 (
    echo ❌ Помилка при запуску Docker!
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ✅ БОТ ЗАПУЩЕНО В DOCKER!                         ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📊 Статус контейнерів:
docker-compose ps
echo.
echo 📋 Корисні команди:
echo.
echo   Переглядати логи бота:
echo   $ docker-compose logs -f bot
echo.
echo   Зупинити контейнери:
echo   $ docker-compose down
echo.
echo   Перезапустити:
echo   $ docker-compose restart
echo.
echo ✅ БОТ ГОТОВИЙ! Пишіть йому /start в Telegram 🎵
echo.

pause
