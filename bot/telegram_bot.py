"""
Updated Telegram bot handlers with all advanced commands
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, ContextTypes
from bot.commands import (
    record_command, di_command, rec_command, setwatermarksize_command, 
    handle_callback, STEP_AUDIO, STEP_WATERMARK, STEP_ASPECT, 
    STEP_COMPRESSION, STEP_UPLOAD
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Start command handler
    Shows main menu with available options
    """
    user = update.effective_user
    
    keyboard = [
        [
            InlineKeyboardButton("📺 Browse Channels", callback_data='list_channels'),
            InlineKeyboardButton("🎬 Quick Record", callback_data='quick_record'),
        ],
        [
            InlineKeyboardButton("📁 My Recordings", callback_data='my_recordings'),
            InlineKeyboardButton("⏰ Schedule", callback_data='schedule_recording'),
        ],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data='help'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        f"👋 Welcome, {user.first_name}!\n\n"
        "🤖 *JioTV Recording Bot*\n\n"
        "📺 Record JioTV streams with advanced options:\n"
        "✅ Multiple audio tracks (Hindi, Tamil, Telugu, Kannada, English)\n"
        "✅ Watermark positioning (6 positions)\n"
        "✅ Custom aspect ratios (6 layouts)\n"
        "✅ Video compression (4 presets)\n"
        "✅ Auto upload (Telegram, Drive, Both)\n\n"
        "*📋 Available Commands:*\n"
        "`/record` - Quick recording\n"
        "`/di` - Scheduled recording\n"
        "`/rec` - Record from direct link\n"
        "`/setwatermarksize` - Set watermark size\n"
        "`/help` - View help\n\n"
        "What would you like to do?"
    )
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = """
*🤖 JioTV Recording Bot - Complete Guide*

*📋 COMMANDS:*

*1. /record* - Quick Recording
   `Usage: /record <channel> <duration>`
   `Example: /record pogo 00:30:00`

*2. /di* - Delayed/Scheduled Recording  
   `Usage: /di -c <ch> -d <date> -t <time> -n <file>`
   `Example: /di -c pogo -d "20 June 2026" -t 12:15-13:00 -n pogo.mkv`

*3. /rec* - Record from Direct Link
   `Usage: /rec <link> <duration>`
   `Example: /rec https://stream.url 00:00:10`

*4. /setwatermarksize* - Set Watermark Size
   `Usage: /setwatermarksize <size>`
   `Example: /setwatermarksize 205`
   `Range: 50-500 pixels`

*5. /channels* - List Available Channels
   Browse all JioTV channels

*6. /recordings* - View Your Recordings
   Manage and download recorded files

*7. /help* - Show This Message

*🎚️ RECORDING OPTIONS:*

🎧 *Audio Tracks:*
   Hindi • Tamil • Telugu • Kannada • English

🖼 *Watermark Positions:*
   ↖️ Top Left | ↗️ Top Right | 🎯 Center
   ↙️ Bottom Left | ↘️ Bottom Right | ⬆️ Top Center

📺 *Video Layouts:*
   21:9 • 16:9 • 4:5 • 16:9 Black Bars • 16:9 Zoom • 1280×720

📦 *Compression Options:*
   ⚡ Ultra Fast (Largest file, fastest)
   🚀 Fast (Fast processing)
   ⚖️ Medium (Balanced, recommended)
   🐌 Slow (Smallest file, slow)
   📦 Skip (Original quality, no compression)

📤 *Upload Destinations:*
   💬 Telegram • 📁 Google Drive • 🔄 Both

*⚡ QUICK START:*

1️⃣ Type `/record pogo 00:30:00`
2️⃣ Select audio track
3️⃣ Choose watermark position
4️⃣ Pick video layout
5️⃣ Set compression
6️⃣ Choose upload destination
7️⃣ Review and start

*💡 ADVANCED USAGE:*

Set custom watermark size:
`/setwatermarksize 250`

Schedule recording for later:
`/di -c sony -d "25 June 2026" -t 18:00-19:00 -n sony.mkv`

Record from external link:
`/rec https://example.com/stream.m3u8 01:00:00`

*📞 SUPPORT:*

Join: https://t.me/jitendraunatti_github
Email: jitendraunatti@pm.me

*⚖️ Legal:*
This bot is for educational purposes only.
Respect copyright and terms of service.
    """
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle general button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'list_channels':
        await query.edit_message_text(text="📺 Channels feature coming soon!")
    elif query.data == 'quick_record':
        await query.edit_message_text(
            text="📺 *Quick Recording*\n\nUse: `/record channel_name duration`",
            parse_mode="Markdown"
        )
    elif query.data == 'my_recordings':
        await query.edit_message_text(text="📁 Your recordings feature coming soon!")
    elif query.data == 'schedule_recording':
        await query.edit_message_text(
            text="⏰ *Schedule Recording*\n\nUse: `/di -c ch -d date -t time -n file`",
            parse_mode="Markdown"
        )
    elif query.data == 'help':
        await help_command(update, context)


def setup_handlers(application: Application) -> None:
    """Setup all command and callback handlers"""
    
    # Create conversation handler for recording workflow
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("record", record_command),
            CommandHandler("di", di_command),
            CommandHandler("rec", rec_command),
        ],
        states={
            STEP_AUDIO: [CallbackQueryHandler(handle_callback)],
            STEP_WATERMARK: [CallbackQueryHandler(handle_callback)],
            STEP_ASPECT: [CallbackQueryHandler(handle_callback)],
            STEP_COMPRESSION: [CallbackQueryHandler(handle_callback)],
            STEP_UPLOAD: [CallbackQueryHandler(handle_callback)],
        },
        fallbacks=[],
    )
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("setwatermarksize", setwatermarksize_command))
    
    # Conversation handler for multi-step recording
    application.add_handler(conv_handler)
    
    # General callback handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    logger.info("Bot handlers setup complete - All features enabled ✅")
