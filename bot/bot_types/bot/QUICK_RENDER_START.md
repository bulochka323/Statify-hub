# 🚀 QUICK START: Запуск з мовами на Render.com

## 5 ХВИЛИН - LIVE НА RENDER.COM! 🎉

---

## ✅ ПЕРЕДУМОВИ

- 📱 **Telegram Bot** (від @BotFather) - має `BOT_TOKEN`
- 🎵 **Spotify App** - має `CLIENT_ID` & `CLIENT_SECRET`
- 💻 **GitHub репо** - код загруженний
- 🌐 **Render.com акаунт** - безплатно на https://render.com

---

## STEP 1: Підготовка (2 хвилини)

### 1.1 GitHub

```bash
# У корені проекту:
git add .
git commit -m "Add: Multi-language + Render.com ready"
git push origin main
```

### 1.2 Spotify Settings

1. Перейти: https://developer.spotify.com/dashboard
2. Вибрати вашу App
3. **Edit Settings** → **Redirect URIs** додати:
```
https://your-render-service-name.onrender.com/callback
```

---

## STEP 2: Render.com Databases (2 хвилини)

### 2.1 PostgreSQL

```
Render Dashboard → New + → PostgreSQL
  Name: statify-hub-db
  Region: Frankfurt (або найближчий)
  Plan: Free
  [Create]
  
Копіювати: "Internal Database URL"
```

### 2.2 Redis

```
Render Dashboard → New + → Redis
  Name: statify-hub-redis
  Region: Frankfurt (один як PostgreSQL!)
  Plan: Free
  [Create]
  
Копіювати: "Internal Redis URL"
```

⏳ **Чекати 3-5 хвилин, поки БД готуються...**

---

## STEP 3: Web Service (1 хвилина)

### 3.1 Створіть Web Service

```
Render Dashboard → New + → Web Service
  GitHub: [Connect GitHub]
  - Авторизуватися
  - Обрати: statify-hub (ваш репо)
  
  Name: statify-hub-bot
  Region: Frankfurt (як БД!)
  Branch: main
  Root Directory: bot ⚠️ ВАЖЛИВО!
  
  Runtime: Python 3
  Build: pip install -r requirements.txt
  Start: python main.py & uvicorn api.handlers:app --host 0.0.0.0 --port 10000
  
  Plan: Free
  [Create Web Service]
```

---

## STEP 4: Environment Variables (1 хвилина)

**На Render.com в Web Service налаштуваннях:**

Додайте кожну змінну окремо:

```
BOT_TOKEN
  = ВАШ_TOKEN_ВІД_BOTFATHER

SPOTIFY_CLIENT_ID
  = ВАШ_CLIENT_ID_ВІД_SPOTIFY

SPOTIFY_CLIENT_SECRET
  = ВАШ_SECRET_ВІД_SPOTIFY

SPOTIFY_REDIRECT_URI
  = https://statify-hub-bot.onrender.com/callback

DATABASE_URL
  = postgresql://... (від PostgreSQL на render.com)

REDIS_URL
  = redis://... (від Redis на render.com)

ADMIN_IDS
  = ВАШ_TELEGRAM_ID (з /start в боті)

DEFAULT_LANGUAGE
  = uk

LOG_LEVEL
  = INFO

RENDER_HOST
  = 0.0.0.0

RENDER_PORT
  = 10000
```

⏳ **Deploy почнеться автоматично!**

---

## STEP 5: Перевірка (видалено!)

```
⏳ Чекати 3-5 хвилин на Render Dashboard → Logs
```

**Успіх коли:**
```
Bot started!
```

**Помилка?** Дивіться Logs на Render.com 👆

---

## 🎉 ГОТОВО!

### Тест в Telegram:

```
Знайти: @YourBotName
/start
↓
Виберіть мову:
🇺🇦 Українська
🇵🇱 Polska
🇬🇧 English
↓
Вибрати мову
↓
🎵 Підключити Spotify → авторизуватися
↓
📊 Тепер у вас є боти!
```

---

## 📊 МОВИ

Користувачи можуть:
- ✅ Вибрати мову при **першому старті**
- ✅ Змінити мову в **⚙️ Налаштування → 🌐 Мова**
- ✅ Весь контент буде у **вибраній мові**

**Поддержані мови:**
- 🇺🇦 Українська (uk)
- 🇵🇱 Polska (pl)
- 🇬🇧 English (en)

---

## 🔄 ОНОВЛЕННЯ

Кожен `git push` → автоматичний deploy на render.com!

```bash
# Змінили щось?
git add .
git commit -m "Fix: something"
git push origin main

# На Render Dashboard за 1-2 хвилини буде новий deploy! 🚀
```

---

## ⚠️ ПОТОЧНІ ПОМИЛКИ

| Помилка | Рішення |
|---------|--------|
| "Bot doesn't respond" | Перевіріьте `BOT_TOKEN` + Логи на Render |
| "Database error" | DATABASE_URL скопійована правильно? Чи БД готова? |
| "Spotify callback fails" | URL в Spotify Settings точний? |
| "No language choice" | Міграція БД запущена? (алембік) |

Див. **LOCALIZATION.md** + **RENDER_DEPLOY.md** для деталей!

---

## 📚 ДОКУМЕНТАЦІЯ

- 📖 **READY_FOR_RENDER.md** - що было добавлено
- 📖 **RENDER_DEPLOY.md** - детальна інструкція
- 📖 **LOCALIZATION.md** - як работают мови

---

## 💰 ЦЕНА

**Free Plan на Render.com:**
- ✅ 750 часів/місяць на один Web Service
- ✅ PostgreSQL 256 MB
- ✅ Redis 256 MB
- ✅ Автоматичні SSL сертифікати (HTTPS)

Якщо потрібно більше → **Pay As You Go** ($7/місяц)

---

Made with ❤️ for Statify Hub
© 2026 Statify Hub Team 🎵

**STATUS: ✅ LIVE ON RENDER.COM**
