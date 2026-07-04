"""
Configuration and settings for the JioTV Recording Bot
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', 0)) if os.getenv('ADMIN_USER_ID') else None

# JioTV Configuration
JIOTV_USERNAME = os.getenv('JIOTV_USERNAME', '')
JIOTV_API_BASE = os.getenv('JIOTV_API_BASE', 'https://jiotvapi.media.jio.com')
JIOTV_DEVICE_TYPE = 'web'

# Recording Configuration
RECORDINGS_DIR = os.getenv('RECORDINGS_DIR', './recordings')
MAX_RECORDING_DURATION = int(os.getenv('MAX_RECORDING_DURATION', 3600))  # 1 hour default
VIDEO_QUALITY = os.getenv('VIDEO_QUALITY', 'high')  # high, medium, low
MAX_CONCURRENT_RECORDINGS = int(os.getenv('MAX_CONCURRENT_RECORDINGS', 2))

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./jiotv_bot.db')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'bot.log')

# Create recordings directory if it doesn't exist
os.makedirs(RECORDINGS_DIR, exist_ok=True)
