#!/bin/bash

# ======================================================================
# STATIFY HUB - Автоматична Установка Бота
# ======================================================================
# Цей скрипт встановить всі залежності та налаштує бота
# Вам потрібно тільки вставити дані в .env файл!
# ======================================================================

set -e

cd "$(dirname "$0")"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   STATIFY HUB BOT - SETUP                      ║"
echo "║                  🎵 Spotify Telegram Bot 🎵                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Перевірка Python
echo "[1/6] Перевірка Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не встановлено!"
    echo "   На Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "   На macOS: brew install python3"
    exit 1
fi
python3 --version
echo "✅ Python знайдено!"
echo ""

# Перевірка pip
echo "[2/6] Встановлення pip..."
python3 -m pip install --upgrade pip --quiet
echo "✅ pip оновлено!"
echo ""

# Встановлення залежностей
echo "[3/6] Встановлення залежностей Python (це займе ~ 2-3 хвилини)..."
echo "       Встановлюємо: aiogram, sqlalchemy, asyncpg, redis, pillow, aiohttp..."
pip install -r requirements.txt
echo "✅ Залежності встановлені!"
echo ""

# Налаштування .env
echo "[4/6] Налаштування конфігурації..."
if [ -f .env ]; then
    echo "⚠️  .env файл вже існує. Пропускаємо..."
else
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env файл створено з .env.example"
        echo ""
        echo "⚠️  ВАЖЛИВО: Відредагуйте .env файл та вставте ваші дані:"
        echo "   - BOT_TOKEN (від @BotFather в Telegram)"
        echo "   - SPOTIFY_CLIENT_ID та SPOTIFY_CLIENT_SECRET"
        echo "   - DATABASE_URL та REDIS_URL (якщо не localhost)"
        echo ""
    else
        echo "❌ .env.example не знайдено!"
        exit 1
    fi
fi
echo ""

# Створення папок
echo "[5/6] Створення необхідних папок..."
mkdir -p logs uploads temp
chmod 755 logs uploads temp
echo "✅ Папки створено!"
echo ""

# Перевірка PostgreSQL та Redis
echo "[6/6] Перевірка бази даних..."
echo ""
echo "ℹ️  Переконайтесь, що запущені:"
echo "   📦 PostgreSQL на localhost:5432"
echo "   📦 Redis на localhost:6379"
echo ""
echo "   Якщо використовуєте Docker:"
echo "   $ docker-compose up -d"
echo ""
echo ""

# Завершення
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ✅ ВСТАНОВЛЕННЯ ЗАВЕРШЕНО!                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Наступні кроки:"
echo ""
echo "1️⃣  Відредагуйте .env файл:"
echo "   nano .env"
echo ""
echo "2️⃣  Запустіть PostgreSQL та Redis:"
echo "   - Локально: postgres та redis-server"
echo "   - Docker: docker-compose up -d"
echo ""
echo "3️⃣  Запустіть бота:"
echo "   python3 main.py"
echo ""
echo "4️⃣  Запустіть його з Docker (альтернатива):"
echo "   docker-compose up --build"
echo ""

read -p "Запустити бота зараз? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Запуск бота..."
    python3 main.py
else
    echo ""
    echo "Готово! Запустіть python3 main.py коли будете готові."
fi
