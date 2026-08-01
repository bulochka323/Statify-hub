# 🎵 STATIFY HUB - ШВИДКИЙ ГАЙД ЗА 5 ХВИЛИН

## ⚡ КРОК 1: Запуск Setup Скрипту (1 хвилина)

### На Windows:
```powershell
cd bot
.\setup.bat
```

### На Linux/macOS:
```bash
cd bot
chmod +x setup.sh
./setup.sh
```

**Скрипт автоматично:**
- ✅ Встановить усі Python залежності
- ✅ Створить папку `.env` з шаблоном
- ✅ Підготує директорії для логів

---

## ⚡ КРОК 2: Налаштування Spotify (2 хвилини)

### 2.1. Реєстрація у Spotify Developer
1. Перейдіть на https://developer.spotify.com/dashboard
2. Натисніть **"Log In"** → Реєстрація
3. Створіть додаток: **"Create an App"**
4. Прийміть умови та натисніть **"Create"**
5. На сторінці додатку скопіюйте:
   - **Client ID** → в .env як `SPOTIFY_CLIENT_ID`
   - **Client Secret** → в .env як `SPOTIFY_CLIENT_SECRET`

### 2.2. Налаштування Redirect URI
1. На тій же сторінці натисніть **"Edit Settings"**
2. Знайдіть **"Redirect URIs"**
3. Додайте: `http://localhost:8000/callback`
4. Натисніть **"Save"**

---

## ⚡ КРОК 3: Налаштування Telegram (1 хвилина)

### 3.1.创ание бота у BotFather
1. Пишіть **@BotFather** в Telegram
2. Натисніть **/newbot**
3. Введіть ім'я: `Statify Hub Bot`
4. Введіть username: `statify_hub_bot` (или свое)
5. Скопіюйте токен → в .env як `BOT_TOKEN`

Готово! Бот створений.

---

## ⚡ КРОК 4: Налаштування БД (1 хвилина)

### Варіант A: Локально (для розробки)

**Windows (PostgreSQL):**
```powershell
# Скачайте PostgreSQL з https://www.postgresql.org/download/windows/
# Встановіть з:
# - Username: postgres
# - Password: password (як в .env)
```

**macOS:**
```bash
brew install postgresql@16 redis
brew services start postgresql@16
brew services start redis
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install postgresql postgresql-contrib redis-server
sudo systemctl start postgresql
sudo systemctl start redis-server
```

### Варіант B: Docker (рекомендується)
```bash
cd bot
docker-compose up -d
```

Це запустить PostgreSQL та Redis автоматично!

---

## ⚡ КРОК 5: Редагування .env Файлу (1 хвилина)

Відкрийте файл `bot/.env` та вставте свої дані:

```env
# 🤖 Telegram Bot (з BotFather)
BOT_TOKEN=123456789:ABCDefg_HijKLmnoPqrSTuvwxyz

# 🎵 Spotify API (з Developer Dashboard)
SPOTIFY_CLIENT_ID=a1b2c3d4e5f6g7h8i9j0
SPOTIFY_CLIENT_SECRET=x9y8z7w6v5u4t3s2r1q0
SPOTIFY_REDIRECT_URI=http://localhost:8000/callback

# 🗄️ База Даних (якщо використовуєте Docker - залишіть як є)
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/statify_hub
REDIS_URL=redis://localhost:6379

# ⚙️ Інші налаштування
ADMIN_IDS=123456789
LOG_LEVEL=INFO
```

---

## ⚡ КРОК 6: Запуск Бота (ГОТОВО!)

### Варіант 1: Локальний запуск
```powershell
# Windows
cd bot
python main.py

# Linux/macOS
cd bot
python3 main.py
```

### Варіант 2: Docker запуск
```bash
cd bot
docker-compose up
```

---

## ✅ ПЕРЕВІРКА: ЧИ ПРАЦЮЄ БОТ?

1. Пишіть боту команду: **/start**
2. Повинна з'явитися кнопка **"🎵 Підключити Spotify"**
3. Натисніть на кнопку
4. Авторизуйтесь в Spotify
5. Вернеться в бота → **ВСЕ ПРАЦЮЄ!** 🎉

---

## 🆘 ЯКЩО ЩОС НЕ ПРАЦЮЄ

### Помилка: "ModuleNotFoundError: No module named 'aiogram'"
```powershell
pip install -r requirements.txt
```

### Помилка: "Connection refused" для PostgreSQL
- Перевірте, чи запущений PostgreSQL
- `docker-compose up -d` для Docker

### Помилка: "Invalid BOT_TOKEN"
- Перевірте токен від @BotFather
- Він має бути на вигляд: `123456789:ABCDefg...`

### Помилка: "Invalid SPOTIFY_CLIENT_ID"
- Перевірте, чи скопіювали корректно з Dashboard
- Перевірте, чи немає пробілів в .env

### Бот не відповідає
```powershell
# Перевірте логи
type logs/bot.log

# Перезапустіть
# Вийдіть з програми (Ctrl+C)
# Запустіть заново
python main.py
```

---

## 📊 СТРУКТУРА ПРОЕКТУ

```
bot/
├── main.py              👈 ТОЧКА ВХОДУ (запустіть це)
├── .env                 👈 ВАШІ ДАНІ (вставте сюда)
├── requirements.txt     👈 ЗАЛЕЖНОСТІ (встановлюються автоматично)
├── setup.bat/.sh        👈 АВТОМАТИЧНА УСТАНОВКА
├── docker-compose.yml   👈 ДЛЯ DOCKER
├── config/              📁 Налаштування
├── database/            📁 База даних
├── handlers/            📁 Обробники подій
├── services/            📁 Бізнес-логіка
├── spotify/             📁 Spotify API
└── ...
```

---

## 🚀 КОМАНДНІ РЯДКИ

```powershell
# Установка залежностей
pip install -r requirements.txt

# Запуск бота
python main.py

# Запуск з Docker
docker-compose up -d

# Переглянути логи
type logs/bot.log          # Windows
tail -f logs/bot.log       # Linux/macOS

# Тестування
python -m pytest tests/

# Міграції БД
alembic upgrade head
```

---

## 📞 ПОТРІБНА ДОПОМОГА?

Дивіться детальну документацію в `SETUP.md`

---

**Бажаємо вам веселих мелодій! 🎵**
