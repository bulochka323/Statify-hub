# 🎵 Statify Hub Bot - Детальна Інструкція Запуску

## 📋 Кроки Налаштування

### Крок 1: Реєстрація Додатку у Spotify

1. Перейдіть на https://developer.spotify.com/
2. Натисніть **"Log In"** або **"Sign Up"** для реєстрації
3. Прийміть умови і виконайте верифікацію
4. Перейдіть в Dashboard і натисніть **"Create an App"**
5. Дайте ім'я додатку (наприклад, "Statify Hub")
6. Приймете умови і натисніть **"Create"**
7. Скопіюйте:
   - **Client ID**
   - **Client Secret**

### Крок 2: Реєстрація Бота у Telegram

1. Пишіть **@BotFather** у Telegram
2. Отримаєте токен на вигляд: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

### Крок 3: Налаштування .env Файлу

Створіть файл `bot/.env` з вашими даними:

```env
# Telegram Bot
BOT_TOKEN=ВАШ_BOT_ТОКЕН

# Spotify API
SPOTIFY_CLIENT_ID=ВАШ_CLIENT_ID
SPOTIFY_CLIENT_SECRET=ВАШ_CLIENT_SECRET
SPOTIFY_REDIRECT_URI=http://localhost:8000/callback

# База Даних
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/statify_hub

# Redis
REDIS_URL=redis://localhost:6379

# Інше
ADMIN_IDS=123456789
LOG_LEVEL=INFO
```

### Крок 4: Установка PostgreSQL та Redis

#### На Windows:

```bash
# Установка PostgreSQL
# Завантажте з https://www.postgresql.org/download/windows/
# Встановіть з дефолтним паролем: password

# Установка Redis
# Завантажте з https://github.com/microsoftarchive/redis/releases
# або використайте WSL2
```

#### На macOS:

```bash
# Установка PostgreSQL
brew install postgresql@16

# Установка Redis
brew install redis

# Запуск
brew services start postgresql@16
brew services start redis
```

#### На Linux (Ubuntu/Debian):

```bash
# Установка PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Установка Redis
sudo apt-get install redis-server

# Запуск
sudo systemctl start postgresql
sudo systemctl start redis-server
```

### Крок 5: Запуск Бота (Локально)

**Windows:**
```cmd
cd bot
run.bat
```

**Linux/macOS:**
```bash
cd bot
bash run.sh
```

**Вручну:**
```bash
cd bot
pip install -r requirements.txt
alembic upgrade head
python main.py
```

### Крок 6: Запуск з Docker

```bash
cd bot
docker-compose up -d
```

## 🔧 Налаштування Spotify Redirect URI

1. Перейдіть у Dashboard вашого додатку Spotify
2. Натисніть **"Edit Settings"**
3. Знайдіть поле **"Redirect URIs"**
4. Додайте: `http://localhost:8000/callback`
5. Натисніть **"Save"**

## 🧪 Тестування Бота

### Запуск тестів

```bash
python -m pytest tests/ -v
```

### Ручне тестування

1. Пишіть боту `/start`
2. Натисніть **"🎵 Підключити Spotify"**
3. Дозвольте доступ до вашого акаунту
4. Переглядайте статистику!

## 📊 Структура Бази Даних

```
Users          - Користувачі
├─ id
├─ telegram_id
├─ spotify_id
├─ level, xp
└─ total_listening_time

Tracks         - Треки
├─ spotify_id
├─ name
└─ artist

UserTrackHistory - Історія прослуховування
├─ user_id
├─ track_spotify_id
└─ play_count

Artists        - Артисти
└─ spotify_id

UserArtistStats  - Статистика артистів
└─ play_count

Genres         - Жанри
└─ name

UserGenreStats - Статистика жанрів
└─ play_count

Achievements   - Досягнення
├─ code
├─ name
└─ condition_type

DailyStats     - Щоденна статистика
├─ listening_time_ms
└─ tracks_played

Friends        - Дружба
├─ user_id
└─ friend_id
```

## 🚀 Деплоймент на Heroku

```bash
#ログування
heroku login

# Створення додатку
heroku create statify-hub

# Додавання PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Додавання Redis
heroku addons:create heroku-redis:premium-0

# Встановлення змінних оточення
heroku config:set BOT_TOKEN=your_token
heroku config:set SPOTIFY_CLIENT_ID=your_id
# ... інші змінні

# Деплоймент
git push heroku main

# Запуск міграцій
heroku run alembic upgrade head
```

## 🚀 Деплоймент на AWS

1. Використовуйте **EC2** для бота
2. **RDS** для PostgreSQL
3. **ElastiCache** для Redis
4. **IAM** для доступів

## 📱 Використання Бота

### Команди
- `/start` - Запуск бота
- Всі інші функції через кнопки (inline keyboards)

### Меню
1. **🏠 Головна** - Дом-сторінка
2. **🎧 Зараз слухаю** - Поточний трек
3. **📊 Статистика** - День/Тиждень/Місяць/Рік
4. **🔥 Топ** - Топ артистів/пісень/альбомів/жанрів
5. **🧠 AI Аналіз** - Персональна аналітика
6. **🏆 Досягнення** - Ваші бейджи
7. **👥 Друзі** - Управління друзями
8. **⚔️ Батл** - Змаганнях з друзями
9. **📅 Wrapped** - Spotify Wrapped
10. **🎨 Картки** - Красиві картинки
11. **⚙️ Налаштування** - Персоналізація

## 🆘 Вирішення Проблем

### Помилка: "Invalid client_id"
- Перевірте `SPOTIFY_CLIENT_ID` у .env файлі
- Переконайтесь, що додаток активний у Spotify Dashboard

### Помилка: "Connection refused" для PostgreSQL
- Запустіть PostgreSQL: `brew services start postgresql@16`
- Проверьте `DATABASE_URL`

### Помилка: "Connection refused" для Redis
- Запустіть Redis: `redis-server`
- Проверьте `REDIS_URL`

### Помилка: "Unauthorized" при авторизації Spotify
- Переконайтесь, що у .env коректні дані
- Перевірте Redirect URI у Spotify Dashboard

## 📚 Документація

- [aiogram Docs](https://docs.aiogram.dev/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

## 💬 Підтримка

Якщо у вас виникли питання:
1. Перевірте логи: `logs/bot.log`
2. Читайте README.md у кожній папці
3. Створіть Issue на GitHub

---

**Бажаємо успіхів! Любіть музику! 🎵**
