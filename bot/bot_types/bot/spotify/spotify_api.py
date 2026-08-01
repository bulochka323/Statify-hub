import aiohttp
from typing import Optional, Dict, Any
from config.settings import settings
from config.logger import logger


class SpotifyAPI:
    """Клієнт для роботи зі Spotify API."""
    
    BASE_URL = "https://api.spotify.com/v1"
    AUTH_URL = "https://accounts.spotify.com/api/token"
    AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
    
    def __init__(self):
        self.client_id = settings.spotify_client_id
        self.client_secret = settings.spotify_client_secret
        self.redirect_uri = settings.spotify_redirect_uri
    
    def get_authorize_url(self) -> str:
        """Отримати URL для авторизації."""
        scopes = [
            "user-read-private",
            "user-read-email",
            "user-read-recently-played",
            "user-top-read",
            "user-library-read",
            "user-read-currently-playing",
        ]
        
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(scopes),
            "show_dialog": "true"
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.AUTHORIZE_URL}?{query_string}"
    
    async def get_access_token(self, code: str) -> Optional[Dict[str, Any]]:
        """Отримати access token за кодом."""
        try:
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.AUTH_URL, data=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to get token: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error getting access token: {e}")
            return None
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Оновити access token."""
        try:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.AUTH_URL, data=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to refresh token: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return None
    
    async def get_current_user(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Отримати інформацію про поточного користувача."""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.BASE_URL}/me", headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to get user: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    async def get_currently_playing(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Отримати трек, що зараз грає."""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.BASE_URL}/me/player/currently-playing",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 204:
                        return None
                    else:
                        logger.error(f"Failed to get currently playing: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error getting currently playing: {e}")
            return None
    
    async def get_recently_played(
        self,
        access_token: str,
        limit: int = 50
    ) -> Optional[Dict[str, Any]]:
        """Отримати недавно прослухані треки."""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {"limit": limit}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.BASE_URL}/me/player/recently-played",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to get recently played: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error getting recently played: {e}")
            return None
    
    async def get_top_items(
        self,
        access_token: str,
        item_type: str = "artists",
        limit: int = 50,
        time_range: str = "medium_term"
    ) -> Optional[Dict[str, Any]]:
        """Отримати топ артистів або треків."""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {"limit": limit, "time_range": time_range}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.BASE_URL}/me/top/{item_type}",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to get top {item_type}: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error getting top items: {e}")
            return None
    
    async def get_track(self, access_token: str, track_id: str) -> Optional[Dict[str, Any]]:
        """Отримати інформацію про трек."""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.BASE_URL}/tracks/{track_id}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to get track: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error getting track: {e}")
            return None
    
    async def get_tracks_audio_features(
        self,
        access_token: str,
        track_ids: list[str]
    ) -> Optional[Dict[str, Any]]:
        """Отримати аудіо характеристики треків."""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {"ids": ",".join(track_ids)}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.BASE_URL}/audio-features",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to get audio features: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error getting audio features: {e}")
            return None
