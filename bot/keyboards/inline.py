from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization.languages import LANGUAGES, get_text


def language_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура вибору мови."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🇺🇦 Українська", callback_data="lang_uk")],
        [InlineKeyboardButton(text=f"🇵🇱 Polska", callback_data="lang_pl")],
        [InlineKeyboardButton(text=f"🇬🇧 English", callback_data="lang_en")],
    ])


def main_menu(language_code: str = "en") -> InlineKeyboardMarkup:
    """Головне меню."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 " + get_text(language_code, "btn_stats"), callback_data="menu_home")],
        [InlineKeyboardButton(text="🎧 Зараз слухаю", callback_data="menu_now_playing")],
        [InlineKeyboardButton(text="📊 " + get_text(language_code, "btn_stats"), callback_data="menu_stats")],
        [InlineKeyboardButton(text="🔥 " + get_text(language_code, "btn_top"), callback_data="menu_top")],
        [InlineKeyboardButton(text="🧠 AI Аналіз", callback_data="menu_ai_analysis")],
        [InlineKeyboardButton(text="🏆 Досягнення", callback_data="menu_achievements")],
        [InlineKeyboardButton(text="👥 " + get_text(language_code, "btn_friends"), callback_data="menu_friends")],
        [InlineKeyboardButton(text="⚔️ " + get_text(language_code, "btn_battles"), callback_data="menu_battle")],
        [InlineKeyboardButton(text="📅 Wrapped", callback_data="menu_wrapped")],
        [InlineKeyboardButton(text="🎨 Картки", callback_data="menu_cards")],
        [InlineKeyboardButton(text="⚙️ " + get_text(language_code, "btn_settings"), callback_data="menu_settings")],
    ])


def start_keyboard(language_code: str = "en") -> InlineKeyboardMarkup:
    """Клавіатура на старті."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎵 " + get_text(language_code, "btn_auth_spotify"), 
            callback_data="auth_spotify"
        )],
        [InlineKeyboardButton(
            text="🌐 " + get_text(language_code, "btn_language"), 
            callback_data="select_language"
        )],
    ])


def stats_period() -> InlineKeyboardMarkup:
    """Вибір періоду для статистики."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 День", callback_data="stats_day")],
        [InlineKeyboardButton(text="📆 Тиждень", callback_data="stats_week")],
        [InlineKeyboardButton(text="📋 Місяць", callback_data="stats_month")],
        [InlineKeyboardButton(text="📊 Рік", callback_data="stats_year")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu_home")],
    ])


def top_period() -> InlineKeyboardMarkup:
    """Вибір періоду для топу."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 День", callback_data="top_day")],
        [InlineKeyboardButton(text="📆 Тиждень", callback_data="top_week")],
        [InlineKeyboardButton(text="📋 Місяць", callback_data="top_month")],
        [InlineKeyboardButton(text="📊 Рік", callback_data="top_year")],
        [InlineKeyboardButton(text="🌍 За весь час", callback_data="top_all_time")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu_home")],
    ])


def top_type() -> InlineKeyboardMarkup:
    """Вибір типу для топу."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎤 Артисти", callback_data="top_type_artists")],
        [InlineKeyboardButton(text="🎵 Пісні", callback_data="top_type_tracks")],
        [InlineKeyboardButton(text="💿 Альбоми", callback_data="top_type_albums")],
        [InlineKeyboardButton(text="🎶 Жанри", callback_data="top_type_genres")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu_top")],
    ])


def wrapped_type() -> InlineKeyboardMarkup:
    """Вибір типу Wrapped."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Щотижнево", callback_data="wrapped_weekly")],
        [InlineKeyboardButton(text="📋 Щомісяця", callback_data="wrapped_monthly")],
        [InlineKeyboardButton(text="📅 Щороку", callback_data="wrapped_yearly")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu_home")],
    ])


def back_button(callback: str = "menu_home") -> InlineKeyboardMarkup:
    """Кнопка назад."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=callback)],
    ])


def settings_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура налаштувань."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Сповіщення", callback_data="settings_notifications")],
        [InlineKeyboardButton(text="🎨 Тема", callback_data="settings_theme")],
        [InlineKeyboardButton(text="🌍 Мова", callback_data="settings_language")],
        [InlineKeyboardButton(text="📱 Профіль", callback_data="settings_profile")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu_home")],
    ])
