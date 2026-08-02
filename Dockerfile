FROM python:3.13-slim

# Встановлюємо необхідні системні інструменти для збірки C/Rust пакетів
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Оновлюємо pip, setuptools та wheel для пошуку готових колес (wheels)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Копіюємо і встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код бота
COPY . .

# Команда для запуску (заміни main.py на твій головний файл, якщо він називається інакше)
CMD ["python", "main.py"]