#!/usr/bin/env python3
"""
STATIFY HUB - Test Setup Script
Перевірка всіх налаштувань перед запуском бота
"""

import sys
import os
from pathlib import Path

# Кольори для виводу
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
CHECK = '✅'
CROSS = '❌'
INFO = 'ℹ️ '

def print_header():
    """Виведення заголовка."""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}║{' '*68}{BLUE}║{RESET}")
    print(f"{BLUE}║  STATIFY HUB BOT - SETUP VERIFICATION{' '*30}{BLUE}║{RESET}")
    print(f"{BLUE}║  🎵 Перевірка налаштувань 🎵{' '*38}{BLUE}║{RESET}")
    print(f"{BLUE}║{' '*68}{BLUE}║{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

def check_python_version():
    """Перевірка версії Python."""
    print(f"{INFO} Перевірка Python...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"{RED}{CROSS} Python 3.10+ потрібен (поточна: {version.major}.{version.minor}){RESET}")
        return False
    
    print(f"{GREEN}{CHECK} Python {version.major}.{version.minor}.{version.micro}{RESET}")
    return True

def check_required_files():
    """Перевірка наявності необхідних файлів."""
    print(f"\n{INFO} Перевірка файлів...")
    
    required_files = [
        '.env',
        'requirements.txt',
        'main.py',
        'config/settings.py',
        'database/db.py',
        'database/models.py',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   {GREEN}{CHECK} {file}{RESET}")
        else:
            print(f"   {RED}{CROSS} {file} (ВІДСУТНІЙ){RESET}")
            all_exist = False
    
    return all_exist

def check_env_file():
    """Перевірка .env файлу."""
    print(f"\n{INFO} Перевірка .env конфігурації...")
    
    if not os.path.exists('.env'):
        print(f"   {RED}{CROSS} .env файл не знайдено!{RESET}")
        return False
    
    required_keys = [
        'BOT_TOKEN',
        'SPOTIFY_CLIENT_ID',
        'SPOTIFY_CLIENT_SECRET',
        'DATABASE_URL',
        'REDIS_URL'
    ]
    
    with open('.env', 'r') as f:
        env_content = f.read()
    
    missing_keys = []
    for key in required_keys:
        if key in env_content:
            # Перевіримо, чи не запоповно значення
            lines = env_content.split('\n')
            for line in lines:
                if line.startswith(key + '='):
                    value = line.split('=', 1)[1].strip()
                    if value and not value.startswith('your_'):
                        print(f"   {GREEN}{CHECK} {key} налаштовано{RESET}")
                    else:
                        print(f"   {YELLOW}⚠️  {key} ще не налаштовано (значення за замовчуванням){RESET}")
                    break
        else:
            missing_keys.append(key)
            print(f"   {RED}{CROSS} {key} не знайдено в .env{RESET}")
    
    return len(missing_keys) == 0

def check_packages():
    """Перевірка встановлених пакетів."""
    print(f"\n{INFO} Перевірка Python пакетів...")
    
    required_packages = [
        'aiogram',
        'sqlalchemy',
        'asyncpg',
        'aiohttp',
        'redis',
        'PIL',
        'alembic',
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            if package == 'PIL':
                __import__('PIL')
                module_name = 'Pillow'
            else:
                __import__(package)
                module_name = package
            
            print(f"   {GREEN}{CHECK} {module_name}{RESET}")
        except ImportError:
            print(f"   {RED}{CROSS} {package} (не встановлено){RESET}")
            all_installed = False
    
    if not all_installed:
        print(f"\n{YELLOW}Встановіть пакети:{RESET}")
        print(f"   pip install -r requirements.txt")
    
    return all_installed

def check_database_connection():
    """Перевірка з'єднання з БД."""
    print(f"\n{INFO} Перевірка бази даних...")
    
    try:
        import asyncpg
        print(f"   {YELLOW}⚠️  asyncpg встановлено (перевірку з'єднання будемо при запуску){RESET}")
        return True
    except ImportError:
        print(f"   {RED}{CROSS} asyncpg не встановлено{RESET}")
        return False

def check_spotify_config():
    """Перевірка Spotify конфігурації."""
    print(f"\n{INFO} Перевірка Spotify налаштувань...")
    
    try:
        from config.settings import settings
        
        if not settings.spotify_client_id or settings.spotify_client_id.startswith('your_'):
            print(f"   {YELLOW}⚠️  SPOTIFY_CLIENT_ID не налаштовано{RESET}")
            return False
        
        if not settings.spotify_client_secret or settings.spotify_client_secret.startswith('your_'):
            print(f"   {YELLOW}⚠️  SPOTIFY_CLIENT_SECRET не налаштовано{RESET}")
            return False
        
        print(f"   {GREEN}{CHECK} Spotify конфігурація налаштована{RESET}")
        return True
    
    except Exception as e:
        print(f"   {RED}{CROSS} Помилка при читанні конфігурації: {e}{RESET}")
        return False

def print_summary(results):
    """Виведення резюме."""
    print(f"\n{BLUE}{'='*70}{RESET}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print(f"{GREEN}✅ ВСІ ПЕРЕВІРКИ ПРОЙДЕНІ! БОТ ГОТОВИЙ ДО ЗАПУСКУ!{RESET}")
        print(f"\n🚀 Запустіть бота командою:")
        print(f"   {BLUE}python main.py{RESET}")
    else:
        print(f"{YELLOW}⚠️  ДЕЯКІ ПЕРЕВІРКИ НЕ ПРОЙДЕНІ{RESET}")
        print(f"\n🔧 Виправте наступне:")
        for check, result in results.items():
            if not result:
                print(f"   {RED}{CROSS} {check}{RESET}")
    
    print(f"\n{BLUE}{'='*70}{RESET}\n")
    
    return all_passed

def main():
    """Головна функція."""
    print_header()
    
    # Запуск перевірок
    results = {
        'Python версія (3.10+)': check_python_version(),
        'Необхідні файли': check_required_files(),
        '.env конфігурація': check_env_file(),
        'Python пакети': check_packages(),
        'Database підтримка': check_database_connection(),
        'Spotify налаштування': check_spotify_config(),
    }
    
    # Виведення резюме
    success = print_summary(results)
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
