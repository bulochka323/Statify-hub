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

# МАГІЯ DOCKER: автоматично перейменовуємо конфліктну папку 'types', 
# щоб Python не плутав її зі стандартною бібліотекою
RUN if [ -d "bot/types" ]; then mv bot/types bot/app_types; fi

# Налаштовуємо шляхи та запуск
ENV PYTHONPATH=/app/bot:/app

CMD ["python", "bot/main.py"]
