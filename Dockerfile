FROM python:3.13-slim

# Встановлюємо системні компілятори (gcc, build-essential) для збірки C/Rust залежностей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Оновлюємо pip, setuptools та wheel для підтягування готових wheels
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Копіюємо requirements.txt з папки bot/
COPY bot/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . .

# Запуск бота (якщо головний файл у папці bot, наприклад bot/main.py — скоригуй шлях)
CMD ["python", "-m", "bot.main"]