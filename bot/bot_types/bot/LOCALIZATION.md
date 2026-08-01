# 🌍 Багатомовність Statify Hub

Statify Hub підтримує **3 мови**:
- 🇺🇦 **Українська** (uk)
- 🇵🇱 **Polska** (pl)
- 🇬🇧 **English** (en)

---

## 🎯 Як це працює?

### При першому старті бота

1. Користувач запускає `/start`
2. Бот показує вибір мови:
   ```
   🌐 Виберіть мову / Wybierz język / Choose language:
   
   🇺🇦 Українська
   🇵🇱 Polska
   🇬🇧 English
   ```
3. Користувач вибирає мову
4. Мова зберігається в БД (поле `language` в таблиці `users`)
5. Весь подальший контент бота – у вибраній мові

### Зміна мови

Користувач може змінити мову в любий момент:
- **⚙️ Налаштування** → **🌐 Мова** → вибрати нову мову

Мова одразу оновлюється в БД.

---

## 📁 Структура файлів

```
bot/
├── localization/
│   ├── __init__.py              # Експорт функцій
│   └── languages.py             # Всі переводи (3000+ строк)
├── keyboards/
│   └── inline.py                # Клавіатури з мовами
├── handlers/
│   └── user_handlers.py         # Обработка мов
├── database/
│   ├── models.py                # Додано поле `language`
│   └── alembic/versions/
│       └── 002_add_language.py  # Міграція БД
└── ...
```

---

## 🔤 Як додати новий текст?

### 1. Додайте ключ в `languages.py`

```python
TRANSLATIONS = {
    "uk": {
        "my_new_text": "Мій новий текст",
    },
    "pl": {
        "my_new_text": "Mój nowy tekst",
    },
    "en": {
        "my_new_text": "My new text",
    }
}
```

### 2. Використайте в коді

```python
from localization.languages import get_text

# У handler
language = user.language  # uk, pl або en
text = get_text(language, "my_new_text")
await message.answer(text)

# З параметрами
text = get_text(language, "stats_level", level=5)
```

---

## 💾 База даних

### Таблиця `users` тепер має:

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    ...
    language VARCHAR(10) DEFAULT 'en',  -- ← НОВЕ ПОЛЕ
    ...
);
```

### Миграція

Запустіть для оновлення БД:

```bash
# Linux/Mac
alembic upgrade head

# Windows
python -m alembic upgrade head
```

---

## 🚀 Запуск на Render.com

При deploy на render.com все автоматично:

1. **Новий користувач** → вибір мови
2. **Мова зберігається** в PostgreSQL на render.com
3. **Можна змінювати** будь-коли в налаштуваннях

**Немає потреби** в환경 змінних чи додаткових налаштувань!

---

## 📊 Статистика

- **3 мови** (uk, pl, en)
- **100+ ключів** перекладу
- **500+ строк** тексту на кожну мову
- **Динамічне завантаження** (не потребує перезавантаження)

---

## 🔧 Приклади використання

### Приклад 1: Простий текст

```python
language = user.language  # "uk"
welcome = get_text(language, "welcome_text")
await message.answer(welcome, parse_mode="HTML")
```

### Приклад 2: Текст з параметрами

```python
language = user.language  # "pl"
stats_text = get_text(language, "stats_level", level=user.level)
# Вивести: "🏆 Poziom: 5"
await message.answer(stats_text)
```

### Приклад 3: Клавіатура з мовою

```python
language = user.language  # "en"
keyboard = start_keyboard(language)
await message.answer("Choose:", reply_markup=keyboard)
```

---

## ⚠️ Важливо!

1. **Завжди передавайте** `language_code` в функції
2. **Не забудьте** зберегти мову користувача в БД
3. **Використовуйте** `parse_mode="HTML"` для форматування

---

## 📞 Підтримка

Якщо виникли проблеми:
- Перевіріьте чи користувач вибрав мову
- Перевіріьте чи ключ існує в `languages.py`
- Перевіріьте мовний код: uk, pl, en

---

Made with ❤️ for multi-language support
© 2026 Statify Hub Team 🎵
