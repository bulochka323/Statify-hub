"""
Localization module for Statify Hub
Поддержка: Українська 🇺🇦, Польська 🇵🇱, English 🇬🇧
"""

LANGUAGES = {
    "uk": "Українська 🇺🇦",
    "pl": "Polska 🇵🇱",
    "en": "English 🇬🇧",
}

TRANSLATIONS = {
    "uk": {
        # Start/Welcome
        "welcome_title": "🎵 Добро пожалувати до Statify Hub!",
        "welcome_text": """🎵 <b>Добро пожалувати до Statify Hub!</b>

Це преміальний Telegram-бот для аналізу твоєї Spotify статистики.

Ми покажемо тобі:
- 📊 Детальну статистику прослуховувань
- 🏆 Твої досягнення та рівень
- 🎤 Топ артистів та пісень
- 🧠 AI аналіз твого смаку
- 👥 Батли та змаганнях з друзями
- 📅 Spotify Wrapped щодня, щотижня, щомісяця

Давайте почнемо! Підключи свій Spotify акаунт 🎵""",
        
        # Language selection
        "select_language": "Виберіть мову / Wybierz język / Choose language:",
        "language_selected": "✅ Мова змінена на Українську 🇺🇦",
        
        # Buttons
        "btn_auth_spotify": "🎵 Підключити Spotify",
        "btn_stats": "📊 Моя статистика",
        "btn_top": "🏆 Топ",
        "btn_battles": "⚔️ Батли",
        "btn_friends": "👥 Друзі",
        "btn_settings": "⚙️ Налаштування",
        "btn_language": "🌐 Мова",
        "btn_help": "❓ Допомога",
        "btn_back": "◀️ Назад",
        "btn_share": "📤 Поділитися",
        "btn_yes": "✅ Так",
        "btn_no": "❌ Ні",
        
        # Auth
        "auth_title": "🎵 Авторизація Spotify",
        "auth_text": """🎵 <b>Авторизація Spotify</b>

Натисніть на посилання нижче, щоб авторизуватися в своєму Spotify акаунті:

<a href="{auth_url}">Авторизуватися в Spotify</a>

Після авторизації ви будете перенаправлені назад до боту.""",
        "auth_success": "✅ Успішно авторизовані в Spotify!",
        "auth_error": "❌ Помилка авторизації. Спробуйте ще раз.",
        
        # Stats
        "stats_title": "📊 Твоя статистика",
        "stats_listening_time": "⏱️ Час прослуховування: <b>{time}</b> годин",
        "stats_total_tracks": "🎵 Всього пісень: <b>{count}</b>",
        "stats_total_artists": "🎤 Всього артистів: <b>{count}</b>",
        "stats_total_genres": "🎨 Жанрів: <b>{count}</b>",
        "stats_level": "🏆 Рівень: <b>{level}</b>",
        "stats_xp": "⭐ XP: <b>{xp}</b>",
        
        # Top
        "top_artists": "🎤 ТОП АРТИСТІВ",
        "top_tracks": "🎵 ТОП ПІСЕНЬ",
        "top_albums": "💿 ТОП АЛЬБОМІВ",
        "top_genres": "🎨 ТОП ЖАНРІВ",
        
        # Time period
        "period_day": "📅 За день",
        "period_week": "📊 За тиждень",
        "period_month": "📈 За місяць",
        "period_year": "📌 За рік",
        "period_all_time": "♾️ За весь час",
        
        # Battles
        "battles_title": "⚔️ Батли",
        "battles_create": "➕ Новий батл",
        "battles_list": "📋 Мої батли",
        "battles_invite": "🎯 Запросити друга",
        
        # Friends
        "friends_title": "👥 Друзі",
        "friends_add": "➕ Додати друга",
        "friends_compatibility": "🎵 Музична сумісність: <b>{percent}%</b>",
        
        # Settings
        "settings_title": "⚙️ Налаштування",
        "settings_notifications": "🔔 Сповіщення",
        "settings_privacy": "🔒 Приватність",
        "settings_theme": "🎨 Тема",
        
        # Common messages
        "error": "❌ Сталась помилка. Спробуйте пізніше.",
        "loading": "⏳ Завантаження...",
        "success": "✅ Успіх!",
        "not_found": "❌ Не знайдено",
        "access_denied": "❌ Доступ заборонено",
        
        # Help
        "help_text": """❓ <b>Довідка</b>

<b>Основні команди:</b>
/start - Початок роботи
/stats - Моя статистика
/top - Топ рейтинги
/battles - Батли
/friends - Друзі
/settings - Налаштування
/help - Ця довідка

<b>Як користуватися:</b>
1️⃣ Авторизуйтесь у Spotify
2️⃣ Чекайте на синхронізацію даних
3️⃣ Переглядайте статистику
4️⃣ Битись з друзями!

<b>Потреба в допомозі?</b>
Напишіть @statify_hub_support""",
    },
    
    "pl": {
        # Start/Welcome
        "welcome_title": "🎵 Witaj w Statify Hub!",
        "welcome_text": """🎵 <b>Witaj w Statify Hub!</b>

To premium bot Telegramowy do analizy Twojej statystyki Spotify.

Pokażemy Ci:
- 📊 Szczegółową statystykę odtworzeń
- 🏆 Twoje osiągnięcia i poziom
- 🎤 Top artystów i piosenek
- 🧠 Analizę AI Twojego smaku
- 👥 Bitwy i konkurencję z przyjaciółmi
- 📅 Spotify Wrapped codziennie, co tydzień, co miesiąc

Zaczynajmy! Połącz swoje konto Spotify 🎵""",
        
        # Language selection
        "select_language": "Wybierz język / Виберіть мову / Choose language:",
        "language_selected": "✅ Język zmieniony na Polski 🇵🇱",
        
        # Buttons
        "btn_auth_spotify": "🎵 Połącz Spotify",
        "btn_stats": "📊 Moja statystyka",
        "btn_top": "🏆 Top",
        "btn_battles": "⚔️ Bitwy",
        "btn_friends": "👥 Przyjaciele",
        "btn_settings": "⚙️ Ustawienia",
        "btn_language": "🌐 Język",
        "btn_help": "❓ Pomoc",
        "btn_back": "◀️ Wstecz",
        "btn_share": "📤 Udostępnij",
        "btn_yes": "✅ Tak",
        "btn_no": "❌ Nie",
        
        # Auth
        "auth_title": "🎵 Autoryzacja Spotify",
        "auth_text": """🎵 <b>Autoryzacja Spotify</b>

Kliknij poniższe łącze, aby zalogować się na swoim koncie Spotify:

<a href="{auth_url}">Zaloguj się w Spotify</a>

Po autoryzacji zostaniesz przekierowany z powrotem do bota.""",
        "auth_success": "✅ Pomyślnie zalogowano w Spotify!",
        "auth_error": "❌ Błąd autoryzacji. Spróbuj jeszcze raz.",
        
        # Stats
        "stats_title": "📊 Twoja statystyka",
        "stats_listening_time": "⏱️ Czas odsłuchu: <b>{time}</b> godzin",
        "stats_total_tracks": "🎵 Razem piosenek: <b>{count}</b>",
        "stats_total_artists": "🎤 Razem artystów: <b>{count}</b>",
        "stats_total_genres": "🎨 Gatunków: <b>{count}</b>",
        "stats_level": "🏆 Poziom: <b>{level}</b>",
        "stats_xp": "⭐ XP: <b>{xp}</b>",
        
        # Top
        "top_artists": "🎤 TOP ARTYSTÓW",
        "top_tracks": "🎵 TOP PIOSENEK",
        "top_albums": "💿 TOP ALBUMÓW",
        "top_genres": "🎨 TOP GATUNKÓW",
        
        # Time period
        "period_day": "📅 Za dzień",
        "period_week": "📊 Za tydzień",
        "period_month": "📈 Za miesiąc",
        "period_year": "📌 Za rok",
        "period_all_time": "♾️ Wszechczasy",
        
        # Battles
        "battles_title": "⚔️ Bitwy",
        "battles_create": "➕ Nowa bitwa",
        "battles_list": "📋 Moje bitwy",
        "battles_invite": "🎯 Zaproś przyjaciela",
        
        # Friends
        "friends_title": "👥 Przyjaciele",
        "friends_add": "➕ Dodaj przyjaciela",
        "friends_compatibility": "🎵 Kompatybilność muzyczna: <b>{percent}%</b>",
        
        # Settings
        "settings_title": "⚙️ Ustawienia",
        "settings_notifications": "🔔 Powiadomienia",
        "settings_privacy": "🔒 Prywatność",
        "settings_theme": "🎨 Motyw",
        
        # Common messages
        "error": "❌ Występił błąd. Spróbuj później.",
        "loading": "⏳ Ładowanie...",
        "success": "✅ Sukces!",
        "not_found": "❌ Nie znaleziono",
        "access_denied": "❌ Dostęp zabroniony",
        
        # Help
        "help_text": """❓ <b>Pomoc</b>

<b>Podstawowe komendy:</b>
/start - Początek
/stats - Moja statystyka
/top - Rankingi Top
/battles - Bitwy
/friends - Przyjaciele
/settings - Ustawienia
/help - Ta pomoc

<b>Jak używać:</b>
1️⃣ Zaloguj się do Spotify
2️⃣ Czekaj na synchronizację danych
3️⃣ Przegladaj statystykę
4️⃣ Walcz z przyjaciółmi!

<b>Potrzebujesz pomocy?</b>
Napisz do @statify_hub_support""",
    },
    
    "en": {
        # Start/Welcome
        "welcome_title": "🎵 Welcome to Statify Hub!",
        "welcome_text": """🎵 <b>Welcome to Statify Hub!</b>

This is a premium Telegram bot for analyzing your Spotify listening statistics.

We'll show you:
- 📊 Detailed listening statistics
- 🏆 Your achievements and level
- 🎤 Top artists and tracks
- 🧠 AI analysis of your taste
- 👥 Battles and competitions with friends
- 📅 Spotify Wrapped daily, weekly, monthly

Let's get started! Connect your Spotify account 🎵""",
        
        # Language selection
        "select_language": "Select language / Виберіть мову / Wybierz język:",
        "language_selected": "✅ Language changed to English 🇬🇧",
        
        # Buttons
        "btn_auth_spotify": "🎵 Connect Spotify",
        "btn_stats": "📊 My Stats",
        "btn_top": "🏆 Top",
        "btn_battles": "⚔️ Battles",
        "btn_friends": "👥 Friends",
        "btn_settings": "⚙️ Settings",
        "btn_language": "🌐 Language",
        "btn_help": "❓ Help",
        "btn_back": "◀️ Back",
        "btn_share": "📤 Share",
        "btn_yes": "✅ Yes",
        "btn_no": "❌ No",
        
        # Auth
        "auth_title": "🎵 Spotify Authorization",
        "auth_text": """🎵 <b>Spotify Authorization</b>

Click the link below to authorize your Spotify account:

<a href="{auth_url}">Authorize Spotify</a>

After authorization, you will be redirected back to the bot.""",
        "auth_success": "✅ Successfully authorized with Spotify!",
        "auth_error": "❌ Authorization error. Please try again.",
        
        # Stats
        "stats_title": "📊 Your Statistics",
        "stats_listening_time": "⏱️ Listening time: <b>{time}</b> hours",
        "stats_total_tracks": "🎵 Total tracks: <b>{count}</b>",
        "stats_total_artists": "🎤 Total artists: <b>{count}</b>",
        "stats_total_genres": "🎨 Genres: <b>{count}</b>",
        "stats_level": "🏆 Level: <b>{level}</b>",
        "stats_xp": "⭐ XP: <b>{xp}</b>",
        
        # Top
        "top_artists": "🎤 TOP ARTISTS",
        "top_tracks": "🎵 TOP TRACKS",
        "top_albums": "💿 TOP ALBUMS",
        "top_genres": "🎨 TOP GENRES",
        
        # Time period
        "period_day": "📅 Per day",
        "period_week": "📊 Per week",
        "period_month": "📈 Per month",
        "period_year": "📌 Per year",
        "period_all_time": "♾️ All time",
        
        # Battles
        "battles_title": "⚔️ Battles",
        "battles_create": "➕ New battle",
        "battles_list": "📋 My battles",
        "battles_invite": "🎯 Invite friend",
        
        # Friends
        "friends_title": "👥 Friends",
        "friends_add": "➕ Add friend",
        "friends_compatibility": "🎵 Music compatibility: <b>{percent}%</b>",
        
        # Settings
        "settings_title": "⚙️ Settings",
        "settings_notifications": "🔔 Notifications",
        "settings_privacy": "🔒 Privacy",
        "settings_theme": "🎨 Theme",
        
        # Common messages
        "error": "❌ An error occurred. Please try later.",
        "loading": "⏳ Loading...",
        "success": "✅ Success!",
        "not_found": "❌ Not found",
        "access_denied": "❌ Access denied",
        
        # Help
        "help_text": """❓ <b>Help</b>

<b>Basic commands:</b>
/start - Get started
/stats - My statistics
/top - Top rankings
/battles - Battles
/friends - Friends
/settings - Settings
/help - This help

<b>How to use:</b>
1️⃣ Log in to Spotify
2️⃣ Wait for data synchronization
3️⃣ View your statistics
4️⃣ Battle with friends!

<b>Need help?</b>
Write to @statify_hub_support""",
    }
}

def get_text(language_code: str, key: str, **kwargs) -> str:
    """
    Get translated text.
    
    Args:
        language_code: Language code (uk, pl, en)
        key: Translation key
        **kwargs: Parameters to format the string
    
    Returns:
        Translated text or key if not found
    """
    if language_code not in TRANSLATIONS:
        language_code = "en"
    
    text = TRANSLATIONS[language_code].get(key, key)
    
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass
    
    return text


def get_language_name(language_code: str) -> str:
    """Get language name."""
    return LANGUAGES.get(language_code, "English")
