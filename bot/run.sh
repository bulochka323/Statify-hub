#!/bin/bash

# Скрипт для запуску бота локально

# Встановлення залежностей
echo "📦 Встановлення залежностей..."
pip install -r requirements.txt

# Запуск міграцій
echo "🗄️ Запуск міграцій БД..."
alembic upgrade head

# Запуск бота
echo "🚀 Запуск бота..."
python main.py
