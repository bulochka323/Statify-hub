@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM                    STATIFY HUB - CLICK TO RUN 🎵
REM  Цей файл встановить і запустить всё за вас! Тільки вставте дані в .env
REM ═══════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

cd /d "%~dp0"

:MENU
cls
color 0A
echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║                                                                           ║
echo ║                 🎵  STATIFY HUB - BOT LAUNCHER  🎵                       ║
echo ║                    Telegram Bot for Spotify Stats                         ║
echo ║                                                                           ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.
echo Виберіть опцію:
echo.
echo   [1] ⚡ QUICK START (установка + запуск)
echo   [2] 🚀 Запустити бота
echo   [3] 🧪 Перевірити налаштування
echo   [4] 📖 Відкрити інструкцію
echo   [5] 🐳 Docker запуск
echo   [6] ⚙️  Редагувати .env
echo   [7] 📚 Dokumentacija
echo   [0] ❌ Вихід
echo.

set /p choice="Введіть номер (0-7): "

if "%choice%"=="1" goto QUICKSTART
if "%choice%"=="2" goto RUN
if "%choice%"=="3" goto TEST
if "%choice%"=="4" goto INSTRUCTIONS
if "%choice%"=="5" goto DOCKER
if "%choice%"=="6" goto EDITENV
if "%choice%"=="7" goto DOCS
if "%choice%"=="0" goto END
goto MENU

:QUICKSTART
cls
echo.
echo 🚀 QUICK START...
echo.
echo [1] Перевірка Python...
python --version
if errorlevel 1 (
    echo ❌ Python не встановлено!
    echo Завантажте з https://www.python.org/
    pause
    goto MENU
)
echo ✅ Python OK
echo.

echo [2] Встановлення залежностей...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ Помилка встановлення!
    pause
    goto MENU
)
echo ✅ Залежності OK
echo.

echo [3] Перевірка .env...
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ .env створено з .env.example
    )
)
echo.

echo [4] Перевірка налаштувань...
python test_setup.py
echo.

echo [5] Запуск бота...
python main.py
goto MENU

:RUN
cls
echo.
echo 🚀 Запуск STATIFY HUB Бота...
echo.
python main.py
if errorlevel 1 (
    echo.
    echo ❌ Помилка! Перевірте:
    echo    1. Чи встановлені залежності (опція 1)
    echo    2. Чи налаштований .env (опція 6)
    echo    3. Чи запущена БД (docker-compose up -d)
    echo.
    pause
)
goto MENU

:TEST
cls
echo.
echo 🧪 Перевірка налаштувань...
echo.
python test_setup.py
echo.
pause
goto MENU

:INSTRUCTIONS
cls
echo.
echo 📖 Відкриття інструкції...
start INSTRUCTIONS.txt
timeout /t 1
goto MENU

:DOCKER
cls
echo.
echo 🐳 Docker Launcher
echo.
call docker-start.bat
goto MENU

:EDITENV
cls
echo.
echo ⚙️  Редагування .env
echo.
if exist .env (
    start notepad .env
) else (
    echo ❌ .env не знайдено!
    if exist .env.example (
        echo Копіюємо з .env.example...
        copy .env.example .env
        start notepad .env
    )
)
echo.
pause
goto MENU

:DOCS
cls
echo.
echo 📚 Документація
echo.
echo Доступні файли:
echo   1. QUICK_START.md
echo   2. SETUP.md
echo   3. README.md
echo   4. CHECKLIST.md
echo.
set /p doc="Виберіть файл (1-4): "
if "%doc%"=="1" start QUICK_START.md
if "%doc%"=="2" start SETUP.md
if "%doc%"=="3" start README.md
if "%doc%"=="4" start CHECKLIST.md
timeout /t 1
goto MENU

:END
echo.
echo До зустрічі! 🎵
echo.
exit /b 0
