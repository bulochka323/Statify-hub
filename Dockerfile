FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY bot/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 1. Авто-створення папки logs
RUN mkdir -p /app/logs /app/bot/logs

# 2. Авто-перейменування конфліктної папки types
RUN if [ -d "bot/types" ]; then mv bot/types bot/app_types; fi

# 3. Авто-фікс імпорту F з aiogram
RUN find bot/ -type f -name "*.py" -exec sed -i 's/from aiogram.filters import F/from aiogram import F/g' {} +

ENV PYTHONPATH=/app/bot:/app

# Запускаємо фоновий веб-сервер для Render + самого бота
CMD ["sh", "-c", "python -m http.server 10000 & exec python bot/main.py"]
