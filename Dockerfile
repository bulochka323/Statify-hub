FROM python:3.13-slim

# Встановлюємо необхідні системні компілятори
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Оновлюємо pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Копіюємо requirements.txt з папки bot/
COPY bot/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт
COPY . .

# ТРЮК: вказуємо Python шукати модулі СПОЧАТКУ в системі, а потім у /app/bot
ENV PYTHONPATH=/usr/local/lib/python3.13:/app/bot:/app

# Запускаємо main.py прямо з папки bot
CMD ["python", "bot/main.py"]
