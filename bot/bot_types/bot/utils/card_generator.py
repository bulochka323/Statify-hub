"""
Генерація карток зі статистикою.
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Optional
from io import BytesIO
import os


class CardGenerator:
    """Генератор карток зі статистикою."""
    
    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self.bg_color = (18, 18, 18)  # Темний фон Spotify
        self.text_color = (255, 255, 255)  # Білий текст
        self.accent_color = (30, 215, 96)  # Зелений Spotify
    
    def create_stats_card(
        self,
        username: str,
        level: int,
        xp: int,
        listening_time: str,
        top_artist: str,
        top_track: str,
    ) -> BytesIO:
        """Створити картку зі статистикою."""
        image = Image.new("RGB", (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(image)
        
        # Прості шрифти (замість завантаження)
        try:
            title_font = ImageFont.load_default()
        except:
            title_font = ImageFont.load_default()
        
        # Заголовок
        draw.text(
            (self.width // 2, 100),
            "🎵 STATIFY HUB 🎵",
            fill=self.accent_color,
            anchor="mm"
        )
        
        # Ім'я користувача
        draw.text(
            (self.width // 2, 250),
            username,
            fill=self.text_color,
            anchor="mm"
        )
        
        # Рівень та XP
        draw.text(
            (self.width // 2, 350),
            f"Рівень: {level} | XP: {xp}",
            fill=self.text_color,
            anchor="mm"
        )
        
        # Час прослуховування
        draw.text(
            (self.width // 2, 450),
            f"🎧 Прослухано: {listening_time}",
            fill=self.text_color,
            anchor="mm"
        )
        
        # Топ артист
        draw.text(
            (self.width // 2, 600),
            f"🎤 Топ артист: {top_artist}",
            fill=self.text_color,
            anchor="mm"
        )
        
        # Топ трек
        draw.text(
            (self.width // 2, 700),
            f"🎵 Топ пісня: {top_track}",
            fill=self.text_color,
            anchor="mm"
        )
        
        # Логотип
        draw.text(
            (self.width // 2, self.height - 100),
            "Created with ❤️ Statify Hub Bot",
            fill=self.accent_color,
            anchor="mm"
        )
        
        # Зберегти в BytesIO
        output = BytesIO()
        image.save(output, format="PNG")
        output.seek(0)
        return output
