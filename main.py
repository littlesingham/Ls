#!/usr/bin/env python3
"""
JioTV Recording Bot for Telegram
Main entry point for the bot application
"""

import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application
from bot.telegram_bot import setup_handlers

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot"""
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        raise ValueError("Please set TELEGRAM_BOT_TOKEN in .env file")
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Setup all handlers
    setup_handlers(application)
    
    # Start the bot
    logger.info("Starting JioTV Recording Bot...")
    application.run_polling(allowed_updates=['message', 'callback_query'])


if __name__ == '__main__':
    main()
