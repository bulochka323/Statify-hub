import logging
import os
from config.settings import settings


def setup_logging() -> None:
    """Налаштування логування."""
    # Створюємо папку для логів, якщо її немає
    os.makedirs("logs", exist_ok=True)

    handlers = [
        logging.StreamHandler()  # Обов'язково для Render / Docker
    ]

    # Додаємо файл тільки якщо є можливість у нього писати
    try:
        handlers.append(logging.FileHandler("logs/bot.log", encoding="utf-8"))
    except Exception:
        pass

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )


logger = logging.getLogger("statify_hub")