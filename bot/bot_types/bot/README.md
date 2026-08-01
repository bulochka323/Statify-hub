# Statify Hub - Spotify Telegram Bot 🎵

Преміальний Telegram-бот для аналізу Spotify статистики з AI аналітикою, досягненнями та соціальними функціями.

## 🚀 Функціонал

### Основні фічі
- 🎵 **Зараз слухаю** - Показує трек, що зараз грає
- 📊 **Статистика** - День, тиждень, місяць, рік
- 🔥 **Топ** - Топ артистів, пісень, альбомів, жанрів
- 🧠 **AI Аналіз** - Аналітика музичного смаку
- 🏆 **Досягнення** - 100+ унікальних досягнень
- 👥 **Друзі** - Управління друзями
- ⚔️ **Батл** - Музична сумісність з друзями
- 📅 **Wrapped** - Щотижнево, щомісячно, щороку
- 🎨 **Картки** - Красиві картинки для соцмереж
- ⚙️ **Налаштування** - Персоналізація

### Унікальні Фічі
- 🎵 **Музична сумісність** - % збігу смаків з будь-яким користувачем
- 🔄 **Spotify Replay** - Переглянути що ти слухав у будь-який день
- 📦 **Time Capsule** - Щомісячно зберігаються "знімки" музичного смаку
- 🎭 **Mood Timeline** - Визначення настрою музики
- 🌍 **Глобальні рейтинги** - Змаганнях з іншими користувачами
- 🎖️ **Сезонні досягнення** - Рідкі та тематичні бейджи

## 📋 Технологічний Стек

- **Python 3.13**
- **aiogram 3.x** - Framework для Telegram API
- **SQLAlchemy** - ORM для роботи з БД
- **PostgreSQL** - Основна база даних
- **Redis** - Кеш та队列
- **APScheduler** - Планування завдань
- **Pillow** - Генерація карток
- **Docker** - Контейнеризація

## 📦 Встановлення

### Попередні вимоги
- Python 3.13+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (опціонально)

### Етап 1: Клонування та залежності

```bash
cd bot
pip install -r requirements.txt
```

### Етап 2: Налаштування .env

```bash
cp .env.example .env
# Відредагуйте .env та вставте ваші дані
```

Потрібні параметри:
- `BOT_TOKEN` - Токен від BotFather
- `SPOTIFY_CLIENT_ID` - ID додатку від Spotify
- `SPOTIFY_CLIENT_SECRET` - Secret від Spotify
- `DATABASE_URL` - URL до PostgreSQL
- `REDIS_URL` - URL до Redis

### Етап 3: Ініціалізація БД

```bash
# Используя алембик
alembic upgrade head
```

### Етап 4: Запуск

```bash
python main.py
```

## 🐳 Запуск з Docker

```bash
docker-compose up -d
```

## 📁 Структура Проекту

```
bot/
├── config/              # Налаштування
│   ├── settings.py     # Основні налаштування
│   └── logger.py       # Логування
├── database/            # БД
│   ├── db.py           # Підключення до БД
│   ├── models.py       # SQLAlchemy моделі
│   └── repository.py   # Data Access Layer
├── handlers/            # Обробники подій
│   ├── user_handlers.py
│   └── menu_handlers.py
├── keyboards/           # Клавіатури
│   └── inline.py       # Inline кнопки
├── services/            # Бізнес-логіка
│   └── spotify_service.py
├── spotify/             # Spotify API
│   └── spotify_api.py
├── scheduler/           # Планування завдань
│   └── tasks.py
├── states/              # FSM стани
│   └── states.py
├── middlewares/         # Middleware
│   └── logging_middleware.py
├── utils/               # Утиліти
│   ├── helpers.py
│   └── card_generator.py
├── main.py             # Точка входу
├── requirements.txt    # Python залежності
├── docker-compose.yml  # Docker Compose
├── Dockerfile          # Docker image
└── .env.example        # Приклад .env
```

## 🔧 Розробка

### Додавання нового обробника

```python
# handlers/my_handler.py
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import F

router = Router()

@router.callback_query(F.data == "my_action")
async def handle_my_action(callback: CallbackQuery):
    await callback.message.answer("Hello!")
    await callback.answer()
```

### Додавання нового middleware

```python
# middlewares/my_middleware.py
from aiogram import BaseMiddleware
from aiogram.types import Update

class MyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Логіка до
        result = await handler(event, data)
        # Логіка після
        return result
```

## 📊 API Endpoints (для webhook)

При потребі може бути інтегрований webhook замість polling:

```
POST /webhook/telegram - Отримання оновлень від Telegram
POST /callback - OAuth callback від Spotify
GET /stats - Публічна статистика користувача
```

## 🔐 Безпека

- ✅ OAuth авторизація Spotify
- ✅ Токени зберігаються в БД (шифровані)
- ✅ Admin-only команди
- ✅ Rate limiting
- ✅ Input validation
- ✅ HTTPS для всіх API запитів

## 📈 Продуктивність

- ✅ Асинхронний код (asyncio)
- ✅ Connection pooling (SQLAlchemy)
- ✅ Кеширование (Redis)
- ✅ Оптимізовані запити до БД
- ✅ Lazy loading даних

## 🛣️ Дорожна Карта

- [ ] Web інтерфейс для статистики
- [ ] AI рекомендації (ML модель)
- [ ] Export даних (CSV, JSON)
- [ ] Інтеграція з Discord
- [ ] Преміум підписка
- [ ] Лідерборди по регіонах
- [ ] Музичні челенджі
- [ ] Інтеграція з Last.fm

## 📝 Ліцензія

MIT License - дивиться `LICENSE` файл

## 👨‍💻 Автор

Створено командою Senior Backend, UX/UI, DevOps інженерів 🚀

## 📞 Контакти

- Telegram Bot: @statify_hub_bot
- GitHub: github.com/yourusername/statify-hub

---

**Made with ❤️ for music lovers** 🎵
