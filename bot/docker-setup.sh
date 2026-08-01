#!/bin/bash
# ======================================================================
# STATIFY HUB - Docker Setup Script
# ======================================================================
# Цей скрипт встановлює та запускає бота в Docker
# Не потрібно встановлювати Python, PostgreSQL або Redis локально!
# ======================================================================

set -e

cd "$(dirname "$0")"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           STATIFY HUB BOT - DOCKER SETUP                       ║"
echo "║                  🐳 Docker Edition 🐳                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Перевірка Docker
echo "[1/3] Перевірка Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не встановлено!"
    echo "   Завантажте з https://www.docker.com/products/docker-desktop"
    exit 1
fi
docker --version
echo "✅ Docker знайдено!"
echo ""

# Налаштування .env
echo "[2/3] Налаштування конфігурації..."
if [ -f .env ]; then
    echo "⚠️  .env файл вже існує. Пропускаємо..."
else
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env файл створено!"
    fi
fi
echo ""

# Запуск Docker Compose
echo "[3/3] Запуск Docker контейнерів..."
echo ""
echo "⚠️  ВАЖЛИВО: Перед запуском відредагуйте .env та вставте:"
echo "   - BOT_TOKEN"
echo "   - SPOTIFY_CLIENT_ID та SPOTIFY_CLIENT_SECRET"
echo ""

read -p "Відредагували .env? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Відредагуйте .env та запустіть скрипт заново."
    exit 1
fi

echo ""
echo "🚀 Запуск контейнерів (це займе 1-2 хвилини на першому запуску)..."
docker-compose up -d

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ✅ БОТ ЗАПУЩЕНО В DOCKER!                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Статус контейнерів:"
docker-compose ps
echo ""
echo "📋 Корисні команди:"
echo ""
echo "   Переглядати логи бота:"
echo "   $ docker-compose logs -f bot"
echo ""
echo "   Зупинити контейнери:"
echo "   $ docker-compose down"
echo ""
echo "   Перезапустити:"
echo "   $ docker-compose restart"
echo ""
echo "✅ БОТ ГОТОВИЙ! Пишіть йому /start в Telegram 🎵"
echo ""
