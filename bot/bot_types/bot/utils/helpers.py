"""
Утиліти для бота.
"""

def format_time(milliseconds: int) -> str:
    """Форматувати час з мілісекунд."""
    total_seconds = milliseconds // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    if hours > 0:
        return f"{hours}ч {minutes}м"
    elif minutes > 0:
        return f"{minutes}м {seconds}с"
    else:
        return f"{seconds}с"


def format_listening_time(milliseconds: int) -> dict:
    """Розділити час прослуховування на компоненти."""
    total_seconds = milliseconds // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    return {
        "hours": hours,
        "minutes": minutes,
        "total_minutes": milliseconds // 1000 // 60
    }


def truncate_text(text: str, max_length: int = 100) -> str:
    """Обрізати текст."""
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text
