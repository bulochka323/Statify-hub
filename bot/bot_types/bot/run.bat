@echo off
REM Скрипт для запуску бота локально на Windows

REM Встановлення залежностей
echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Запуск міграцій
echo.
echo 🗄️ Running database migrations...
alembic upgrade head

REM Запуск бота
echo.
echo 🚀 Starting bot...
python main.py

pause
