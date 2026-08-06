import logging
from typing import Optional

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.inline import language_keyboard, main_menu, start_keyboard
from localization.languages import LANGUAGES, get_text
from services.spotify_service import SpotifyService, UserService
from spotify.spotify_api import SpotifyAPI
from states.states import UserState

# Якщо logger не завантажиться з конфігу, використовуємо стандартний
try:
    from config.logger import logger
except ImportError:
    logger = logging.getLogger(__name__)

router = Router()
spotify_api = SpotifyAPI()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: Optional[AsyncSession] = None):
    """Обробка команди /start."""
    try:
        if not session:
            logger.warning("DbSessionMiddleware не передав session у cmd_start")
            await message.answer("❌ Сталась помилка БД. Спробуйте пізніше.")
            return

        user_service = UserService(session)
        user = await user_service.register_user(
            telegram_id=message.from_user.id,
            display_name=message.from_user.full_name
        )

        # Якщо мова не встановлена, показуємо вибір мови
        if not user or not user.language:
            welcome_text = f"{get_text('en', 'welcome_title')}{get_text('en', 'select_language')}\n"
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
async def handle_language_selection(callback: CallbackQuery, state: FSMContext, session: Optional[AsyncSession] = None):
    """Обробка вибору мови."""
    try:
        if not session:
            await callback.answer("❌ Помилка з'єднання з БД", show_alert=True)
            return

        language_code = callback.data.split("_")[1]  # lang_uk -> uk

        user_service = UserService(session)
        await user_service.update_user(
            telegram_id=callback.from_user.id,
            language=language_code
        )

        # Показуємо привітання на обраній мові
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
async def handle_select_language(callback: CallbackQuery, state: FSMContext, session: Optional[AsyncSession] = None):
    """Обробка кнопки вибору мови."""
    try:
        if not session:
            await callback.answer("❌ Помилка з'єднання з БД", show_alert=True)
            return

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
async def handle_spotify_auth(callback: CallbackQuery, state: FSMContext, session: Optional[AsyncSession] = None):
    """Обробка кнопки авторизації Spotify."""
    try:
        if not session:
            await callback.answer("❌ Помилка з'єднання з БД", show_alert=True)
            return

        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.id)
        language = user.language if user else "en"

        # ✅ Прокидаємо telegram_id у state
        auth_url = spotify_api.get_authorize_url(state=str(callback.from_user.id))

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
        if session:
            user_service = UserService(session)
            user = await user_service.get_user(callback.from_user.id)
            language = user.language if user else "en"
            error_text = get_text(language, "error")
            await callback.message.answer(error_text)
        else:
            await callback.message.answer("❌ Помилка авторизації.")
    finally:
        await callback.answer()


@router.callback_query(F.data == "menu_home")
async def handle_main_menu(callback: CallbackQuery, session: Optional[AsyncSession] = None):
    """Обробка кнопки головного меню."""
    try:
        if not session:
            await callback.answer("❌ Помилка з'єднання з БД", show_alert=True)
            return

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

        menu_text = f"🏠 <b>Головне Меню</b>\n\n👤 <b>{user.display_name}</b>"
        await callback.message.edit_text(
            menu_text,
            reply_markup=main_menu(language),
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Error in handle_main_menu: {e}")
        await callback.answer("❌ Сталась помилка.", show_alert=True)
    finally:
        await callback.answer()