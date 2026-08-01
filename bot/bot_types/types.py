"""
Type definitions for better IDE support
"""

from typing import TypeDict, Optional, List


class UserData(TypeDict):
    """Дані користувача."""
    id: int
    telegram_id: int
    display_name: Optional[str]
    level: int
    xp: int
    total_listening_time: float


class TrackData(TypeDict):
    """Дані треку."""
    id: str
    name: str
    artist: str
    album: str
    duration_ms: int
    image_url: Optional[str]
    url: Optional[str]


class ArtistData(TypeDict):
    """Дані артиста."""
    id: str
    name: str
    image_url: Optional[str]
    url: Optional[str]


class StatsData(TypeDict):
    """Дані статистики."""
    period: str
    listening_time: int
    track_count: int
    artist_count: int
    genre_count: int


class BattleData(TypeDict):
    """Дані батла."""
    user1_id: int
    user2_id: int
    compatibility: float
    common_artists: List[str]
    common_tracks: List[str]
