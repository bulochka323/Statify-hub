# ✅ STATIFY HUB - ФІНАЛЬНИЙ ЧЕКЛИСТ

## 🎯 Перш ніж запускати бота, переконайтесь що ви виконали:

### 📝 ПЕРЕВІРКА ПЕРЕД ЗАПУСКОМ:

- [ ] **Python встановлено**
  - Запустіть: `python --version`
  - Потрібна версія 3.10 або новіша
  - Якщо нема: https://www.python.org/

- [ ] **Git встановлено** (опціонально)
  - Запустіть: `git --version`
  - Для завантаження коду

- [ ] **Spotify账户**
  - Маєте активний Spotify акаунт
  - Якщо нема: https://www.spotify.com/

- [ ] **Telegram**
  - Маєте Telegram встановлено
  - Якщо нема: https://telegram.org/

---

## 🔑 КРОК 1: Отримання Spotify Ключів

- [ ] **Перейдіть на** https://developer.spotify.com/dashboard
- [ ] **Увійдіть або зареєструйтесь**
- [ ] **Натисніть** "Create an App"
- [ ] **Введіть назву**: Statify Hub
- [ ] **Прийміть умови** та створіть
- [ ] **Скопіюйте Client ID** (збережіть где-то)
- [ ] **Скопіюйте Client Secret** (збережіть де-то)
- [ ] **Натисніть** "Edit Settings"
- [ ] **Додайте Redirect URI**: `http://localhost:8000/callback`
- [ ] **Натисніть** "Save"

**✅ Spotify налаштовано!**

---

## 🤖 КРОК 2: Створення Telegram Бота

- [ ] **Пишіть в Telegram** @BotFather
- [ ] **Натисніть** /newbot
- [ ] **Введіть ім'я**: Statify Hub Bot
- [ ] **Введіть username**: statify_hub_bot
- [ ] **Скопіюйте Token** (збережіть де-то)

**✅ Telegram бот створено!**

---

## 🚀 КРОК 3: Установка Залежностей

### Варіант A: Автоматично (РЕКОМЕНДУЄТЬСЯ)

- [ ] **Відкрийте PowerShell/Command Prompt**
- [ ] **Перейдіть в папку з ботом**: `cd bot`
- [ ] **Запустіть**: `.\setup.bat` (Windows) або `./setup.sh` (Linux/Mac)
- [ ] **Дочекайтесь завершення** (~2-3 хвилини)

### Варіант B: Вручну

- [ ] **Запустіть**: `pip install -r requirements.txt`
- [ ] **Дочекайтесь завершення**

**✅ Залежності встановлені!**

---

## ⚙️ КРОК 4: Налаштування .env Файлу

- [ ] **Відкрийте файл** `bot/.env`
- [ ] **Вставте Spotify дані**:
  ```env
  SPOTIFY_CLIENT_ID=a1b2c3d4e5f6g7h8i9j0
  SPOTIFY_CLIENT_SECRET=x9y8z7w6v5u4t3s2r1q0
  ```
- [ ] **Вставте Telegram токен**:
  ```env
  BOT_TOKEN=123456789:ABCDefg_HijKLmnoPqrSTuvwxyz
  ```
- [ ] **Збережіть файл** (Ctrl+S)

**✅ .env налаштовано!**

---

## 🗄️ КРОК 5: Установка БД та Redis

### Варіант A: Docker (НАЙПРОСТІШЕ)

- [ ] **Встановіть Docker Desktop**: https://www.docker.com/products/docker-desktop
- [ ] **Запустіть Docker**
- [ ] **В PowerShell запустіть**: `docker-compose up -d`
- [ ] **Дочекайтесь** (~1 хвилину)

### Варіант B: Локально

**PostgreSQL:**
- [ ] **Завантажте**: https://www.postgresql.org/download/windows/
- [ ] **Встановіть** з паролем `password`
- [ ] **Запустіть** PostgreSQL

**Redis:**
- [ ] **Завантажте**: https://github.com/microsoftarchive/redis/releases
- [ ] **Встановіть та запустіть**

**✅ БД та Redis готові!**

---

## 🧪 КРОК 6: Перевірка Налаштувань

- [ ] **Запустіть**: `python test_setup.py`
- [ ] **Перевірте результати**:
  - ✅ Python версія OK
  - ✅ Файли знайдені
  - ✅ .env налаштовано
  - ✅ Пакети встановлені
  - ✅ БД доступна
  - ✅ Spotify налаштовано

**✅ Все налаштовано!**

---

## 🎵 КРОК 7: Запуск Бота

### Варіант A: Звичайний запуск

- [ ] **Запустіть**: `python main.py`
- [ ] **Дочекайтесь** поки з'явиться "Bot started!"

### Варіант B: Docker запуск

- [ ] **Запустіть**: `docker-compose up`
- [ ] **Дочекайтесь** поки з'явиться "Bot started!"

### Варіант C: Просто запустити файл

- [ ] **Запустіть** `start.bat` (Windows)
- [ ] **Або запустіть** `run.sh` (Linux/Mac)

**✅ БОТ ЗАПУЩЕНО!**

---

## 📱 КРОК 8: Тестування

- [ ] **Відкрийте Telegram**
- [ ] **Напишіть своєму боту** `/start`
- [ ] **Повинна з'явитися** кнопка "🎵 Підключити Spotify"
- [ ] **Натисніть на неї**
- [ ] **Авторизуйтесь в Spotify**
- [ ] **Поверніться в бота**
- [ ] **Переглядайте статистику!**

**🎉 ГОТОВО! БОТ ПРАЦЮЄ!**

---

## 🆘 ЯКЩО ЩОС НЕ ПРАЦЮЄ:

| Проблема | Розв'язання |
|----------|-----------|
| "Python not found" | Встановіть Python з https://www.python.org/ |
| "ModuleNotFoundError" | Запустіть `pip install -r requirements.txt` |
| "Connection refused" (БД) | Запустіть `docker-compose up -d` |
| "Invalid BOT_TOKEN" | Перевірте токен від @BotFather |
| "Invalid client_id" | Перевірте дані в Spotify Dashboard |
| Бот не відповідає | Перевірте логи: `type logs/bot.log` |

---

## 📊 КОМАНДИ ДЛЯ УПРАВЛІННЯ

```powershell
# Запуск бота
python main.py

# Тестування
python test_setup.py

# Docker
docker-compose up -d
docker-compose down
docker-compose logs -f bot

# Переглянути логи
type logs/bot.log
tail -f logs/bot.log      # Linux/Mac

# Встановити залежності
pip install -r requirements.txt

# Оновити залежності
pip install --upgrade -r requirements.txt
```

---

## ✅ ГОТОВО!

Якщо ви виконали всі кроки:
- ✅ Python встановлено
- ✅ Spotify ключі отримано
- ✅ Telegram бот створено
- ✅ Залежності встановлені
- ✅ .env налаштовано
- ✅ БД готова
- ✅ Бот запущено

**🎵 Тепер насолоджуйтесь ботом!**

---

## 📚 БІЛЬШЕ ІНФОРМАЦІЇ:

- `QUICK_START.md` - Швидкий старт за 5 хвилин
- `SETUP.md` - Детальна інструкція
- `README.md` - Про бота та функціонал
- `INSTRUCTIONS.txt` - Повна інструкція для Windows

---

**Успіхів! 🚀**
