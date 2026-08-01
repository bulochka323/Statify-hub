from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    """Стани користувача."""
    SELECT_LANGUAGE = State()
    START = State()
    MAIN_MENU = State()
    SPOTIFY_AUTH = State()
    AWAITING_SPOTIFY_CODE = State()


class StatsState(StatesGroup):
    """Стани для статистики."""
    VIEW_PERIOD = State()
    VIEW_STATS = State()


class TopState(StatesGroup):
    """Стани для топу."""
    SELECT_PERIOD = State()
    SELECT_TYPE = State()
    VIEW_TOP = State()


class BattleState(StatesGroup):
    """Стани для батла."""
    SELECT_OPPONENT = State()
    SELECT_TYPE = State()
    VIEW_BATTLE = State()


class WrappedState(StatesGroup):
    """Стани для Wrapped."""
    SELECT_TYPE = State()
    VIEW_WRAPPED = State()
