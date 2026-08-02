from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from config.logger import logger


class LoggingMiddleware(BaseMiddleware):
    """Middleware для логування всіх оновлень."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            logger.info(f"Message ID {event.message_id} from user {event.from_user.id}")
        elif isinstance(event, CallbackQuery):
            logger.info(f"Callback data '{event.data}' from user {event.from_user.id}")
        else:
            logger.info(f"Event: {type(event).__name__}")

        return await handler(event, data)