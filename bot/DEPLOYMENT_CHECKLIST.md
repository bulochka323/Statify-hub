# ✅ DEPLOYMENT CHECKLIST: Render.com + Multi-Language

## 📝 ПО ПЕРЕД DEPLOYMENT

### ШАГ 1: Локальная проверка (5 минут)

- [ ] `cd bot && pip install -r requirements.txt`
- [ ] Создать `.env` файл (скопировать из `.env.example`)
- [ ] Заполнить: `BOT_TOKEN`, `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`
- [ ] `alembic upgrade head` (запустить миграции)
- [ ] `python main.py` (тест локально)
- [ ] Отправить `/start` в Telegram
- [ ] Выбрать язык (uk, pl, или en)
- [ ] Проверить, что язык сохранился (перезагрузить бота)

### ШАГ 2: Подготовка GitHub (5 минут)

- [ ] `git status` (проверить изменения)
- [ ] `git add .`
- [ ] `git commit -m "Add: Multi-language + Render.com support"`
- [ ] `git push origin main`
- [ ] Проверить на https://github.com, что файлы загружены

### ШАГ 3: Spotify Settings (3 минуты)

- [ ] Перейти: https://developer.spotify.com/dashboard
- [ ] Выбрать вашу App
- [ ] **Edit Settings**
- [ ] **Redirect URIs** → Добавить:
  ```
  https://your-service-name.onrender.com/callback
  ```
- [ ] **Save**

### ШАГ 4: Render.com - PostgreSQL (3 минуты)

- [ ] Перейти: https://render.com
- [ ] **Dashboard** → **New +** → **PostgreSQL**
- [ ] Заполнить:
  - [ ] Name: `statify-hub-db`
  - [ ] Region: Frankfurt (или ближайший)
  - [ ] Plan: **Free**
- [ ] **Create Database**
- [ ] ⏳ Ждать 2-3 минуты
- [ ] Скопировать **Internal Database URL**
- [ ] Сохранить в безопасном месте

### ШАГ 5: Render.com - Redis (3 минуты)

- [ ] **Dashboard** → **New +** → **Redis**
- [ ] Заполнить:
  - [ ] Name: `statify-hub-redis`
  - [ ] Region: **Frankfurt** (как PostgreSQL!)
  - [ ] Plan: **Free**
- [ ] **Create Redis**
- [ ] ⏳ Ждать 1-2 минуты
- [ ] Скопировать **Internal Redis URL**
- [ ] Сохранить в безопасном месте

### ШАГ 6: Render.com - Web Service (5 минут)

- [ ] **Dashboard** → **New +** → **Web Service**
- [ ] **Connect GitHub:**
  - [ ] Нажать: **Connect GitHub**
  - [ ] Авторизоваться
  - [ ] Выбрать репо: `statify-hub`
- [ ] Заполнить:
  - [ ] Name: `statify-hub-bot`
  - [ ] Region: **Frankfurt** (как БД!)
  - [ ] Branch: `main`
  - [ ] Root Directory: **bot** ⚠️ ВАЖНО!
  - [ ] Runtime: `Python 3`
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `python main.py & uvicorn api.handlers:app --host 0.0.0.0 --port 10000`
  - [ ] Plan: **Free**
- [ ] **Create Web Service**

### ШАГ 7: Environment Variables (5 минут)

**На Render.com в Web Service:**

- [ ] **BOT_TOKEN** = ваш токен от @BotFather
- [ ] **SPOTIFY_CLIENT_ID** = из Spotify Developer Dashboard
- [ ] **SPOTIFY_CLIENT_SECRET** = из Spotify Developer Dashboard
- [ ] **SPOTIFY_REDIRECT_URI** = `https://statify-hub-bot.onrender.com/callback`
- [ ] **DATABASE_URL** = из PostgreSQL (Internal Database URL)
- [ ] **REDIS_URL** = из Redis (Internal Redis URL)
- [ ] **ADMIN_IDS** = ваш Telegram ID
- [ ] **DEFAULT_LANGUAGE** = `uk` (или pl, en)
- [ ] **LOG_LEVEL** = `INFO`
- [ ] **RENDER_HOST** = `0.0.0.0`
- [ ] **RENDER_PORT** = `10000`

### ШАГ 8: Deploy (5-10 минут)

- [ ] Нажать **Create Web Service**
- [ ] ⏳ Ждать deploy (3-5 минут)
- [ ] Проверить **Logs** → должно быть `Bot started!`

### ШАГ 9: Тест в Telegram (2 минуты)

- [ ] Найти вашего бота в Telegram: `@YourBotName`
- [ ] Отправить: `/start`
- [ ] Проверить:
  - [ ] Появился выбор языков
  - [ ] Можно выбрать 🇺🇦 Украинский
  - [ ] Можно выбрать 🇵🇱 Polski
  - [ ] Можно выбрать 🇬🇧 English
- [ ] Выбрать язык
- [ ] Проверить, что все тексты на выбранном языке
- [ ] Тапнуть: **🎵 Підключити Spotify** (или equiv. на выбранном языке)
- [ ] Авторизоваться в Spotify
- [ ] Проверить, что callback работает

### ШАГ 10: Дополнительные проверки (3 минуты)

- [ ] API Health Check: `https://statify-hub-bot.onrender.com/api/v1/health`
  - [ ] Должно вернуть: `{"status":"ok"}`
- [ ] Проверить Logs на Render.com
- [ ] Убедиться, что нет ошибок

---

## 🐛 РЕШЕНИЕ ПРОБЛЕМ

### Проблема: "Bot doesn't respond"

**Проверить:**
- [ ] BOT_TOKEN правильный?
- [ ] Logs на Render.com → ищите ошибки
- [ ] config/settings.py файл валиден?
- [ ] requirements.txt установлены?

**Решение:**
```bash
# На Render Dashboard:
1. Перейти в Web Service → Logs
2. Ищить строку "Bot started!"
3. Если ошибка - прочитать сообщение об ошибке
```

### Проблема: "Database connection error"

**Проверить:**
- [ ] DATABASE_URL скопирована правильно?
- [ ] PostgreSQL создан и готов?
- [ ] Изменены ли символы @ или : в URL?

**Решение:**
```
1. На Render Dashboard → PostgreSQL
2. Скопировать снова: "Internal Database URL"
3. Заменить в Environment Variables
4. Перезагрузить Web Service
```

### Проблема: "Redis connection failed"

**Проверить:**
- [ ] REDIS_URL скопирована правильно?
- [ ] Redis создан и готов?

**Решение:**
```
1. На Render Dashboard → Redis
2. Скопировать снова: "Internal Redis URL"
3. Заменить в Environment Variables
4. Перезагрузить Web Service
```

### Проблема: "Spotify callback не работает"

**Проверить:**
- [ ] URL в Spotify Settings: `https://statify-hub-bot.onrender.com/callback`
- [ ] SPOTIFY_REDIRECT_URI в env variables = тому же?
- [ ] Logs показывают callback запрос?

**Решение:**
```
1. В Spotify Developer Dashboard
2. Edit Settings → Redirect URIs
3. Убедиться, что это точно: https://your-service.onrender.com/callback
4. Save
5. Попробовать /start → авторизация снова
```

### Проблема: "Language doesn't persist"

**Проверить:**
- [ ] Миграция БД запущена? `alembic upgrade head`
- [ ] В PostgreSQL есть поле `language`?
- [ ] Пользователь выбрал язык?

**Решение:**
```
1. На Render Dashboard → PostgreSQL
2. Проверить, что БД создана
3. На Render Dashboard → Web Service → Logs
4. Ищить: "Initializing database..."
5. Если нет - база не инициализирована
```

### Проблема: "Deploy fails with error"

**Проверить:**
- [ ] Root Directory = `bot`?
- [ ] requirements.txt существует?
- [ ] main.py существует?
- [ ] Нет Python ошибок в коде?

**Решение:**
```
1. На локальном компьютере: python main.py
2. Если работает локально - значит сервис Render.com
3. Проверить Logs на Render.com
4. Если нужна переиспытание - нажать "Manual Deploy"
```

---

## 📞 БЫСТРЫЕ КОМАНДЫ

### Локальный тест
```bash
cd bot
pip install -r requirements.txt
alembic upgrade head
python main.py
```

### Отправить на GitHub
```bash
git add .
git commit -m "Update: something"
git push origin main
```

### Проверить, что находится в Render.com
```bash
# На Render Dashboard:
# 1. Web Service → Logs (live)
# 2. Web Service → Events (historia)
# 3. PostgreSQL → Data (查看 БД)
```

---

## ✅ УСПЕШНЫЙ DEPLOY ВЫГЛЯДИТ ТАК:

```
✅ Web Service создан на render.com
✅ PostgreSQL готов
✅ Redis готов
✅ Bot запущен (Logs: "Bot started!")
✅ Telegram bot отвечает на /start
✅ Выбор языков работает
✅ Spotify авторизация работает
✅ API health check возвращает {"status":"ok"}
```

---

## 🎉 ГОТОВО!

После выполнения всех пунктов:

1. ✅ Ваш бот live на https://statify-hub-bot.onrender.com
2. ✅ Многоязычный (uk, pl, en)
3. ✅ Автоматический deploy при git push
4. ✅ Production-ready
5. ✅ Масштабируемый

**Тепер можно:**
- 🎉 Пригласить друзей
- 📱 Поделиться ботом
- 🚀 Добавлять новые фичи
- 📊 Смотреть статистику на Render.com

---

**STATUS: ✅ DEPLOYMENT READY**

Если возникли вопросы - см. документацию:
- QUICK_RENDER_START.md
- RENDER_DEPLOY.md
- LOCALIZATION.md
