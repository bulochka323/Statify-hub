# 🚀 Деплой на Render.com

## ✅ Переваги Render.com для Statify Hub

- ✅ **HTTPS автоматично** - Spotify приймає
- ✅ **Безплатний план** - PostgreSQL + Redis + Node.js
- ✅ **Автоматичні оновлення** - GitHub push = автоматичний deploy
- ✅ **Нема IP блокувань** - Spotify API працює
- ✅ **Простий setup** - 5 хвилин

---

## 📋 Передумови

1. **GitHub репозиторій** (fork або новий)
2. **Spotify Developer App** - готові Client ID & Secret
3. **Render.com акаунт** - https://render.com (безплатний)

---

## 🎯 ШАГ 1: Підготовка до GitHub

### 1.1 Клонуйте/залийте код на GitHub

```bash
# Якщо немає репо:
git init
git add .
git commit -m "Initial commit: Statify Hub"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/statify-hub.git
git push -u origin main
```

### 1.2 Переконайтесь, що є `bot/` директорія

Структура повинна бути:
```
statify-hub/
├── bot/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── config/
│   ├── database/
│   ├── handlers/
│   └── ...
```

---

## 🌐 ШАГ 2: Створення сервісів на Render.com

### 2.1 Логіниться на Render.com

1. Перейти на https://render.com
2. Sign Up (або Sign In)
3. Підтвердити емейл

### 2.2 Створити PostgreSQL Database

1. **Dashboard** → **New +** → **PostgreSQL**
2. Назвати: `statify-hub-db`
3. **Region**: обрати найближчий до вас
4. **Plan**: Free
5. **Create Database**
6. ⏳ Чекати 2-3 хвилини
7. **Скопіювати** `Internal Database URL` (потрібна для `.env`)

### 2.3 Створити Redis Cache

1. **Dashboard** → **New +** → **Redis**
2. Назвати: `statify-hub-redis`
3. **Region**: той же, що БД
4. **Plan**: Free
5. **Create Redis**
6. ⏳ Чекати 1-2 хвилини
7. **Скопіювати** `Internal Redis URL` (потрібна для `.env`)

### 2.4 Створити Web Service (Bot + API)

1. **Dashboard** → **New +** → **Web Service**
2. **Підключити GitHub репо**:
   - Вибрати **Connect GitHub** 
   - Авторизуватися
   - Обрати `statify-hub` репо
3. **Налаштування**:
   - **Name**: `statify-hub-bot`
   - **Region**: той же
   - **Branch**: `main`
   - **Root Directory**: `bot` ⚠️ ВАЖЛИВО
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py & uvicorn api.handlers:app --host 0.0.0.0 --port 10000`
   - **Plan**: Free (або付费)
4. **Додати Environment Variables** (натисніть **Add Environment Variable**):

```
BOT_TOKEN                    = ВАШ_BOT_TOKEN_ВІД_BOTFATHER
SPOTIFY_CLIENT_ID           = ВАШ_CLIENT_ID_ВІД_SPOTIFY
SPOTIFY_CLIENT_SECRET       = ВАШ_SECRET_ВІД_SPOTIFY
SPOTIFY_REDIRECT_URI        = https://statify-hub-bot.onrender.com/callback
DATABASE_URL                = postgresql://... (від шага 2.2)
REDIS_URL                   = redis://... (від шага 2.3)
ADMIN_IDS                   = ВАШ_TELEGRAM_ID
DEFAULT_LANGUAGE            = uk
LOG_LEVEL                   = INFO
RENDER_HOST                 = 0.0.0.0
RENDER_PORT                 = 10000
```

5. **Create Web Service**
6. ⏳ Чекати 3-5 хвилин (перший деплой довгий)

---

## 🔐 ШАГ 3: Налаштування Spotify

### 3.1 Перейти на Spotify Developer Dashboard

https://developer.spotify.com/dashboard

### 3.2 Оновити Redirect URI

1. Натисніть на вашу App
2. **Edit Settings**
3. **Redirect URIs** замінити на:
   ```
   https://statify-hub-bot.onrender.com/callback
   ```
4. **Save**

### 3.3 Скопіювати Client ID & Secret

Залиште ці дані для крока 2.4

---

## ✅ ШАГ 4: Перевірка

1. **Render Dashboard** → відкрийте `statify-hub-bot`
2. **Logs** - перевіряйте, що немає помилок
3. Повинна бути строчка: `Bot started!`
4. Оберіть URL вашого сервісу: `https://statify-hub-bot.onrender.com`
5. Перейдіть на: `https://statify-hub-bot.onrender.com/api/v1/health`
6. Повинен вивести: `{"status":"ok"}`

---

## 🤖 ШАГ 5: Запуск бота та вибір мови

### Тест в Telegram

1. Знайти `@YOUR_BOT_NAME` в Telegram
2. Натиснути **/start**
3. **Вибрати мову** 🌐
   - 🇺🇦 Українська
   - 🇵🇱 Polska
   - 🇬🇧 English
4. Бот проведе інші налаштування
5. Якщо все働く - **ВСЕ РАБОТАЕТ!** 🎉

### Про мови

Statify Hub тепер **багатомовний**!

Користувачи можуть:
- ✅ Вибрати мову при першому старті
- ✅ Змінити мову в любий момент в ⚙️ **Налаштування** → 🌐 **Мова**
- ✅ Всі тексти боту буде у вибраній мові

**Поддержані мови:**
- 🇺🇦 Українська (uk)
- 🇵🇱 Polska (pl)
- 🇬🇧 English (en)

Для деталей - див. **LOCALIZATION.md** 📖

### Проглядання логів

```bash
# На Render Dashboard:
# Вибрати Web Service → Logs → дивитися live
```

---

## 🔄 Автоматичні оновлення

**Преимущество Render.com:**
- Кожен **git push** на `main` гілку = автоматичний переdeploй
- Немає потреби вручну перезавантажувати

```bash
# Змініть код локально
git add .
git commit -m "Fix: something"
git push origin main

# Автоматично deploy почнеться! 🚀
```

---

## 🐛 Поточні проблеми

### Проблема: "Bot not responding"

**Рішення:**
- Перевіриьте `BOT_TOKEN` у `.env` - правильний?
- Перевіріьте **Logs** на Render.com
- Перевіріьте, чи немає помилок в `config/settings.py`

### Проблема: "Spotify callback не працює"

**Рішення:**
- Переконайтесь, що URL точний: `https://statify-hub-bot.onrender.com/callback`
- Перевіріьте в Spotify Dashboard Settings
- Логи на Render повинні показати callback

### Проблема: "Мова не зберігається"

**Рішення:**
- Перевіріьте, що міграція БД запущена: `alembic upgrade head`
- Перевіріьте, що поле `language` є в таблиці `users`
- Перевіріьте логи на Render.com



### Проблема: "Database connection error"

**Рішення:**
- Перевіріьте `DATABASE_URL` в `.env`
- Переконайтесь, що БД готова (не в процесі створення)
- Знову додайте `DATABASE_URL` в Render Dashboard Environment

### Проблема: "Redis connection failed"

**Рішення:**
- Перевіріьте `REDIS_URL` в `.env`
- Переконайтесь, що Redis готовий
- У `bot/config/settings.py` змініть default:
  ```python
  redis_url: str = "redis://localhost:6379"  # ← дозволяє локальний fallback
  ```

---

## 💰 Кошти на Render.com

**Free Plan включає:**
- ✅ 750 часів/місяць на один Web Service
- ✅ PostgreSQL 256 MB
- ✅ Redis 256 MB
- ✅ Автоматичні SSL сертифікати (HTTPS)

**Примітка:** Если у вас витратяться 750 часів, сервис буде паузуватися. Решение:
- Обновить до **Pay As You Go** ($7/месяц)
- Або запустити на тому ж ПК (не буде витрат)

---

## 📚 Корисні посилання

- 📖 [Render Docs](https://render.com/docs)
- 🐘 [PostgreSQL на Render](https://render.com/docs/databases)
- 💾 [Redis на Render](https://render.com/docs/redis)
- 🤖 [Telegram Bot API](https://core.telegram.org/bots)
- 🎵 [Spotify Web API](https://developer.spotify.com/documentation/web-api)

---

## 🎉 Вітаємо!

Statify Hub тепер работает на **HTTPS** з **RENDER.COM**! 🚀

Ви можете показати бота друзям і не хвилюватися про те, що комп вимкнеться!

**Що далі?**
1. Пригласіть друзів в бот
2. Додайте нові фічі
3. Покажіть на GitHub ⭐

---

Made with ❤️ for music lovers
© 2026 Statify Hub Team 🎵
