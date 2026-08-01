from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from states.states import UserState
from keyboards.inline import start_keyboard, main_menu, language_keyboard
from services.spotify_service import UserService, SpotifyService
from spotify.spotify_api import SpotifyAPI
from localization.languages import get_text, LANGUAGES
from config.logger import logger

router = Router()
spotify_api = SpotifyAPI()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    """Обробка команди /start."""
    try:
        user_service = UserService(session)
        user = await user_service.register_user(
            telegram_id=message.from_user.id,
            display_name=message.from_user.full_name
        )

        # Якщо мова не встановлена, показуємо вибір мови
        if not user.language:
            welcome_text = f"""
{get_text('en', 'welcome_title')}

{get_text('en', 'select_language')}
            """
            await message.answer(welcome_text, reply_markup=language_keyboard())
            await state.set_state(UserState.SELECT_LANGUAGE)
        else:
            language = user.language
            welcome_text = get_text(language, "welcome_text")
            await message.answer(welcome_text, reply_markup=start_keyboard(language), parse_mode="HTML")
            await state.set_state(UserState.START)

    except Exception as e:
        logger.error(f"Error in cmd_start: {e}")
        await message.answer("❌ Сталась помилка. Спробуйте пізніше.")


@router.callback_query(F.data.startswith("lang_"))
async def handle_language_selection(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обробка вибору мови."""
    try:
        language_code = callback.data.split("_")[1]  # lang_uk -> uk

        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.id)

        if user:
            user.language = language_code
            await user_service.update_user(user)

        # Показуємо привіт на обраній мові
        welcome_text = get_text(language_code, "welcome_text")
        confirmation = get_text(language_code, "language_selected")

        await callback.message.edit_text(
            f"{confirmation}\n\n{welcome_text}",
            reply_markup=start_keyboard(language_code),
            parse_mode="HTML"
        )
        await state.set_state(UserState.START)

    except Exception as e:
        logger.error(f"Error in handle_language_selection: {e}")
        await callback.answer("❌ Помилка", show_alert=True)
    finally:
        await callback.answer()


@router.callback_query(F.data == "select_language")
async def handle_select_language(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обробка кнопки вибору мови."""
    try:
        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.id)
        language = user.language if user else "en"

        text = get_text(language, "select_language")
        await callback.message.edit_text(text, reply_markup=language_keyboard())
        await state.set_state(UserState.SELECT_LANGUAGE)

    except Exception as e:
        logger.error(f"Error in handle_select_language: {e}")
        await callback.answer("❌ Помилка", show_alert=True)
    finally:
        await callback.answer()


@router.callback_query(F.data == "auth_spotify")
async def handle_spotify_auth(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обробка кнопки авторизації Spotify."""
    try:
        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.id)
        language = user.language if user else "en"

        auth_url = spotify_api.get_authorize_url()

        auth_text = get_text(language, "auth_text").format(auth_url=auth_url)

        await callback.message.edit_text(
            auth_text,
            reply_markup=None,
            disable_web_page_preview=True,
            parse_mode="HTML"
        )

        await state.set_state(UserState.AWAITING_SPOTIFY_CODE)

    except Exception as e:
        logger.error(f"Error in handle_spotify_auth: {e}")
        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.id)
        language = user.language if user else "en"
        error_text = get_text(language, "error")
        await callback.message.answer(error_text)
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_home")
async def handle_main_menu(callback: CallbackQuery, session: AsyncSession):
    """Обробка кнопки головного меню."""
    try:
        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.id)
        language = user.language if user else "en"

        if not user or not user.spotify_id:
            welcome_text = get_text(language, "welcome_text")
            await callback.message.edit_text(
                welcome_text,
                reply_markup=start_keyboard(language),
                parse_mode="HTML"
            )
            await callback.answer()
            return

        menu_text = f"""
🏠 **Головне Меню**

👤 **{user.display_name}**
📊 Рівень: {user.level}

⭐ XP: {user.xp}
🎧 Прослухано годин: {user.total_listening_time // 60 // 60}

Виберіть опцію нижче:
        """
        
        await callback.message.edit_text(menu_text, reply_markup=main_menu())
        
    except Exception as e:
        logger.error(f"Error in handle_main_menu: {e}")
        await callback.message.answer("❌ Сталась помилка. Спробуйте пізніше.")
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_now_playing")
async def handle_now_playing(callback: CallbackQuery, session: AsyncSession):
    """Обробка кнопки 'Зараз слухаю'."""
    try:
        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.id)
        
        if not user or not user.spotify_access_token:
            await callback.message.edit_text("❌ Потрібна авторизація")
            await callback.answer()
            return
        
        spotify_service = SpotifyService(session)
        now_playing = await spotify_service.get_currently_playing_info(user.spotify_access_token)
        
        if not now_playing:
            text = "🎵 Зараз ви нічого не слухаєте"
        else:
            text = f"""
🎵 **Зараз слухаєте:**

**{now_playing['name']}**
🎤 {now_playing['artist']}
💿 {now_playing['album']}

⏱️ {now_playing['progress_ms'] // 1000 // 60}:{now_playing['progress_ms'] // 1000 % 60:02d} / {now_playing['duration_ms'] // 1000 // 60}:{now_playing['duration_ms'] // 1000 % 60:02d}

[Слухати на Spotify](SPOTIFY_URL)
            """.replace("SPOTIFY_URL", now_playing['url'] or "#")
        
        from keyboards.inline import back_button
        await callback.message.edit_text(text, reply_markup=back_button("menu_home"))
        
    except Exception as e:
        logger.error(f"Error in handle_now_playing: {e}")
        await callback.message.answer("❌ Сталась помилка. Спробуйте пізніше.")
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_stats")
async def handle_stats(callback: CallbackQuery):
    """Обробка кнопки статистики."""
    try:
        from keyboards.inline import stats_period
        text = "📊 **Виберіть період для статистики:**"
        await callback.message.edit_text(text, reply_markup=stats_period())
    except Exception as e:
        logger.error(f"Error in handle_stats: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()


@router.callback_query(F.data.startswith("stats_"))
async def handle_stats_period(callback: CallbackQuery, session: AsyncSession):
    """Обробка вибору періоду статистики."""
    try:
        period = callback.data.split("_")[1]
        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.id)
        
        if not user or not user.spotify_access_token:
            await callback.message.answer("❌ Потрібна авторизація")
            await callback.answer()
            return
        
        period_names = {
            "day": "Сьогодні",
            "week": "Цей тиждень",
            "month": "Цей місяць",
            "year": "Цей рік"
        }
        
        spotify_service = SpotifyService(session)
        
        # Простий приклад статистики
        if period == "day":
            listening_time = await spotify_service.history_repo.get_total_listening_time(session, user.id, days=1)
        elif period == "week":
            listening_time = await spotify_service.history_repo.get_total_listening_time(session, user.id, days=7)
        elif period == "month":
            listening_time = await spotify_service.history_repo.get_total_listening_time(session, user.id, days=30)
        else:
            listening_time = await spotify_service.history_repo.get_total_listening_time(session, user.id)
        
        hours = listening_time // 1000 // 60 // 60
        minutes = (listening_time // 1000 // 60) % 60
        
        text = f"""
📊 **Статистика: {period_names[period]}**

🎧 Прослухано: {hours}ч {minutes}м
🎵 Треків: {user.total_tracks}
🎤 Артистів: {user.total_artists}
🎶 Жанрів: {user.total_genres}
        """
        
        from keyboards.inline import back_button
        await callback.message.edit_text(text, reply_markup=back_button("menu_stats"))
        
    except Exception as e:
        logger.error(f"Error in handle_stats_period: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_top")
async def handle_top(callback: CallbackQuery):
    """Обробка кнопки топу."""
    try:
        from keyboards.inline import top_period
        text = "🔥 **Виберіть період для топу:**"
        await callback.message.edit_text(text, reply_markup=top_period())
    except Exception as e:
        logger.error(f"Error in handle_top: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()


@router.callback_query(F.data.startswith("top_"))
async def handle_top_selection(callback: CallbackQuery):
    """Обробка вибору топу."""
    try:
        from keyboards.inline import top_type
        text = "🔥 **Що вас цікавить?**"
        await callback.message.edit_text(text, reply_markup=top_type())
    except Exception as e:
        logger.error(f"Error in handle_top_selection: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_achievements")
async def handle_achievements(callback: CallbackQuery, session: AsyncSession):
    """Обробка кнопки досягнень."""
    try:
        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.id)
        
        if not user:
            await callback.message.answer("❌ Потрібна авторизація")
            await callback.answer()
            return
        
        text = f"""
🏆 **Ваші Досягнення**

🌙 Нічна сова
Прослухав 100 годин після опівночі

🔥 Залежний
Прослухав одну пісню 100 разів

🎶 Меломан
1000 різних пісень

Ваш рівень: {user.level}
Ваш XP: {user.xp}
        """
        
        from keyboards.inline import back_button
        await callback.message.edit_text(text, reply_markup=back_button("menu_home"))
        
    except Exception as e:
        logger.error(f"Error in handle_achievements: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_settings")
async def handle_settings(callback: CallbackQuery):
    """Обробка кнопки налаштувань."""
    try:
        from keyboards.inline import settings_keyboard
        text = "⚙️ **Налаштування**"
        await callback.message.edit_text(text, reply_markup=settings_keyboard())
    except Exception as e:
        logger.error(f"Error in handle_settings: {e}")
        await callback.message.answer("❌ Сталась помилка.")
    finally:
        await callback.answer()
