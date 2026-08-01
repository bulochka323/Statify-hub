from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.filters import F
from config.logger import logger

router = Router()


@router.callback_query(F.data == "menu_friends")
async def handle_friends(callback: CallbackQuery):
    """Обробка меню друзів."""
    try:
        from keyboards.inline import back_button
        text = """
👥 **Друзі**

Додавайте друзів та дивіться їх статистику!

На цей час у вас немає друзів.
        """
        await callback.message.edit_text(text, reply_markup=back_button("menu_home"))
    except Exception as e:
        logger.error(f"Error in handle_friends: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_battle")
async def handle_battle(callback: CallbackQuery):
    """Обробка меню батла."""
    try:
        from keyboards.inline import back_button
        text = """
⚔️ **Музичний Батл**

Запросіть друга на батл та дізнайтесь:
- Хто більше слухає?
- Хто має більше жанрів?
- Музична сумісність (%)

На цей час у вас немає друзів для батлу.
        """
        await callback.message.edit_text(text, reply_markup=back_button("menu_home"))
    except Exception as e:
        logger.error(f"Error in handle_battle: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_wrapped")
async def handle_wrapped(callback: CallbackQuery):
    """Обробка меню Wrapped."""
    try:
        from keyboards.inline import wrapped_type
        text = "📅 **Spotify Wrapped - Вибір типу**"
        await callback.message.edit_text(text, reply_markup=wrapped_type())
    except Exception as e:
        logger.error(f"Error in handle_wrapped: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()


@router.callback_query(F.data.startswith("wrapped_"))
async def handle_wrapped_type(callback: CallbackQuery):
    """Обробка типу Wrapped."""
    try:
        wrapped_type = callback.data.split("_")[1]
        
        period_names = {
            "weekly": "Цей тиждень",
            "monthly": "Цей місяць",
            "yearly": "Цей рік"
        }
        
        from keyboards.inline import back_button
        text = f"""
📅 **Spotify Wrapped - {period_names[wrapped_type]}**

📊 Ваша статистика за {period_names[wrapped_type]}:

🎧 Прослухано: 150 годин
🎵 Топ пісня: Song Name - Artist
🎤 Топ артист: Artist Name
💿 Найбільш прослуховуваний альбом: Album Name

Картка створюється...
        """
        await callback.message.edit_text(text, reply_markup=back_button("menu_wrapped"))
    except Exception as e:
        logger.error(f"Error in handle_wrapped_type: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_ai_analysis")
async def handle_ai_analysis(callback: CallbackQuery):
    """Обробка AI аналізу."""
    try:
        from keyboards.inline import back_button
        text = """
🧠 **AI Аналіз Вашого Смаку**

📈 Аналітика:
- Ти слухаєш сумну музику після 22:00
- Найчастіше ти слухаєш реп у дорозі
- У неділю слухаєш значно більше
- Останній місяць твій смак став різноманітнішим
- Твій музичний настрій зараз: Energetic

💡 Рекомендація:
Ймовірно тобі сподобається новий альбом від Artist Name в жанрі Genre
        """
        await callback.message.edit_text(text, reply_markup=back_button("menu_home"))
    except Exception as e:
        logger.error(f"Error in handle_ai_analysis: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_cards")
async def handle_cards(callback: CallbackQuery):
    """Обробка карток."""
    try:
        from keyboards.inline import back_button
        text = """
🎨 **Красиві Картки**

Складіть красиву картку зі своєю статистикою та поділіться нею!

Доступні варіанти:
- Instagram стиль
- Spotify Wrapped стиль
- Мінімалістичний дизайн

Виберіть варіант та відправимо вам картку готову для публікації!
        """
        await callback.message.edit_text(text, reply_markup=back_button("menu_home"))
    except Exception as e:
        logger.error(f"Error in handle_cards: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()
