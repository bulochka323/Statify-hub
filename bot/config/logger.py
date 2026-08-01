import logging
from config.settings import settings


def setup_logging() -> None:
    """Налаштування логування."""
    logging.basicConfig(
        level=settings.log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot.log'),
            logging.StreamHandler()
        ]
    )


logger = logging.getLogger(__name__)
