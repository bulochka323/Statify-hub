FROM python:3.13-slim

# Встановлюємо системні компілятори для збірки C/Rust залежностей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Оновлюємо pip, setuptools та wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Копіюємо requirements.txt з папки bot/
COPY bot/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . .

# Прописуємо шляхи для Python, щоб він бачив імпорти і з кореня, і з папки bot/
ENV PYTHONPATH=/app/bot:/app

# Запуск бота
CMD ["python", "bot/main.py"]