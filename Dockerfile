FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY bot/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 1. Створення папки logs
RUN mkdir -p /app/logs /app/bot/logs

# 2. Перейменування types
RUN if [ -d "bot/types" ]; then mv bot/types bot/app_types; fi

# 3. Фікс імпорту F з aiogram
RUN find bot/ -type f -name "*.py" -exec sed -i 's/from aiogram.filters import F/from aiogram import F/g' {} +

# 4. ФІКС ПОМИЛКИ МІДДЛВЕРА (заміна event.update_id на event.message_id)
RUN find bot/ -type f -name "*.py" -exec sed -i 's/event.update_id/event.message_id/g' {} +

ENV PYTHONPATH=/app/bot:/app

CMD ["sh", "-c", "python -m http.server $PORT & exec python bot/main.py"]
