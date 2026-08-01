"""
Optional: Web API handlers for stats sharing and admin panel
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import async_session
from database.repository import UserRepository
from config.settings import settings
from config.logger import logger
import json


app = FastAPI(title="Statify Hub API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/users/{user_id}/stats")
async def get_user_stats(user_id: int):
    """Отримати публічну статистику користувача."""
    try:
        async with async_session() as session:
            user_repo = UserRepository()
            user = await user_repo.get_user(session, user_id)
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            return {
                "id": user.id,
                "display_name": user.display_name,
                "profile_image_url": user.profile_image_url,
                "level": user.level,
                "xp": user.xp,
                "total_listening_time": user.total_listening_time,
                "total_tracks": user.total_tracks,
                "total_artists": user.total_artists,
                "total_genres": user.total_genres,
            }
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/callback")
async def spotify_callback(code: str = None, error: str = None, state: str = None):
    """Callback від Spotify для авторизації."""
    if error:
        logger.error(f"Spotify authorization error: {error}")
        return {"error": error}

    if code:
        logger.info(f"Spotify authorization code received: {code[:20]}...")
        return {"status": "authorized", "code": code}

    return {"error": "No authorization code provided"}


@app.get("/api/v1/health")
async def health_check():
    """Перевірка здоровʼя API."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    import os

    host = os.getenv("RENDER_HOST", "0.0.0.0")
    port = int(os.getenv("RENDER_PORT", "10000"))

    uvicorn.run(app, host=host, port=port)
