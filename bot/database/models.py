from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, BigInteger
from database.db import Base


class User(Base):
    """Модель користувача."""
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    spotify_id = Column(String(255), unique=True, nullable=True)
    spotify_access_token = Column(Text, nullable=True)
    spotify_refresh_token = Column(Text, nullable=True)
    username = Column(String(255), nullable=True)
    display_name = Column(String(255), nullable=True)
    profile_image_url = Column(String(500), nullable=True)

    # Language preference
    language = Column(String(10), default="en")  # uk, pl, en

    total_listening_time = Column(Float, default=0)  # у хвилинах
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    total_tracks = Column(Integer, default=0)
    total_artists = Column(Integer, default=0)
    total_genres = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_sync = Column(DateTime, nullable=True)


class Track(Base):
    """Модель треку."""
    __tablename__ = "tracks"
    
    id = Column(Integer, primary_key=True)
    spotify_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(500), nullable=False)
    artist = Column(String(500), nullable=False)
    album = Column(String(500), nullable=True)
    duration_ms = Column(Integer, nullable=False)
    image_url = Column(String(500), nullable=True)
    spotify_url = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class UserTrackHistory(Base):
    """Історія прослуховування треків користувача."""
    __tablename__ = "user_track_history"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    track_spotify_id = Column(String(255), nullable=False)
    play_count = Column(Integer, default=1)
    total_time_ms = Column(Integer, default=0)
    
    first_played = Column(DateTime, default=datetime.utcnow)
    last_played = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Artist(Base):
    """Модель артиста."""
    __tablename__ = "artists"
    
    id = Column(Integer, primary_key=True)
    spotify_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(500), nullable=False)
    image_url = Column(String(500), nullable=True)
    spotify_url = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class UserArtistStats(Base):
    """Статистика артистів користувача."""
    __tablename__ = "user_artist_stats"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    artist_spotify_id = Column(String(255), nullable=False)
    play_count = Column(Integer, default=1)
    total_time_ms = Column(Integer, default=0)
    
    first_played = Column(DateTime, default=datetime.utcnow)
    last_played = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Genre(Base):
    """Модель жанру."""
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)


class UserGenreStats(Base):
    """Статистика жанрів користувача."""
    __tablename__ = "user_genre_stats"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    genre_name = Column(String(255), nullable=False)
    play_count = Column(Integer, default=1)
    total_time_ms = Column(Integer, default=0)
    
    first_played = Column(DateTime, default=datetime.utcnow)
    last_played = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Achievement(Base):
    """Модель досягнення."""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(255), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    emoji = Column(String(10), nullable=False)
    condition_type = Column(String(100), nullable=False)
    condition_value = Column(Integer, nullable=False)
    xp_reward = Column(Integer, default=100)
    rarity = Column(String(50), default="common")  # common, rare, epic, legendary
    
    created_at = Column(DateTime, default=datetime.utcnow)


class UserAchievement(Base):
    """Досягнення користувача."""
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    achievement_id = Column(Integer, nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)


class DailyStats(Base):
    """Щоденна статистика."""
    __tablename__ = "daily_stats"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    
    listening_time_ms = Column(Integer, default=0)
    tracks_played = Column(Integer, default=0)
    new_artists = Column(Integer, default=0)
    new_genres = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class Friend(Base):
    """Модель дружби."""
    __tablename__ = "friends"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    friend_id = Column(BigInteger, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)


class TimeCapule(Base):
    """Time Capsule - знімок музичного смаку."""
    __tablename__ = "time_capules"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    top_tracks = Column(Text, nullable=True)  # JSON
    top_artists = Column(Text, nullable=True)  # JSON
    top_genres = Column(Text, nullable=True)  # JSON
    mood = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
