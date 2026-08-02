FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY bot/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт
COPY . .

# 1. Авто-перейменування конфліктної папки types
RUN if [ -d "bot/types" ]; then mv bot/types bot/app_types; fi

# 2. Авто-фікс помилки Клода з 'from aiogram.filters import F'
RUN find bot/ -type f -name "*.py" -exec sed -i 's/from aiogram.filters import F/from aiogram import F/g' {} +

# Налаштовуємо шляхи та запуск
ENV PYTHONPATH=/app/bot:/app

CMD ["python", "bot/main.py"]
