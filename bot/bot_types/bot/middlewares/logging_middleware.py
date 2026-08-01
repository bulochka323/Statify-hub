from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Any, Awaitable
from config.logger import logger


class LoggingMiddleware(BaseMiddleware):
    """Middleware для логування всіх оновлень."""
    
    async def __call__(
        self,
        handler: Callable[[Update], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        logger.info(f"Update: {event.update_id}")
        return await handler(event, data)
