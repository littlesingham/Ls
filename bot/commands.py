"""
Command handlers for recording configuration
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

logger = logging.getLogger(__name__)

# Conversation states
STEP_AUDIO = 1
STEP_WATERMARK = 2
STEP_ASPECT = 3
STEP_COMPRESSION = 4
STEP_UPLOAD = 5


async def record_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    /record command for quick recording
    Usage: /record pogo 00:30:00
    """
    args = context.args
    
    if not args:
        await update.message.reply_text(
            "📺 *Quick Recording*\n\n"
            "Usage: `/record <channel_name> <duration>`\n\n"
            "Examples:\n"
            "`/record pogo 00:30:00`\n"
            "`/record sony 01:00:00`",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    
    channel_name = args[0]
    duration = args[1] if len(args) > 1 else "00:30:00"
    
    context.user_data['channel_name'] = channel_name
    context.user_data['duration'] = duration
    context.user_data['source'] = 'channel'
    
    return await show_audio_selection(update, context)


async def di_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    /di command for scheduled recording
    Usage: /di -c pogo -d "20 June 2026" -t 12:15-13:00 -n pogo.mkv
    """
    args = context.args
    
    if not args:
        await update.message.reply_text(
            "⏰ *Scheduled Recording*\n\n"
            "Usage: `/di -c channel -d date -t time -n filename`\n\n"
            "Example:\n"
            "`/di -c pogo -d \"20 June 2026\" -t 12:15-13:00 -n pogo.mkv`",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    
    # Parse arguments
    params = {}
    i = 0
    while i < len(args):
        if args[i] == "-c" and i + 1 < len(args):
            params['channel'] = args[i + 1]
            i += 2
        elif args[i] == "-d" and i + 1 < len(args):
            params['date'] = args[i + 1]
            i += 2
        elif args[i] == "-t" and i + 1 < len(args):
            params['time'] = args[i + 1]
            i += 2
        elif args[i] == "-n" and i + 1 < len(args):
            params['filename'] = args[i + 1]
            i += 2
        else:
            i += 1
    
    if not all(k in params for k in ['channel', 'date', 'time', 'filename']):
        await update.message.reply_text("❌ Missing parameters")
        return ConversationHandler.END
    
    context.user_data.update(params)
    context.user_data['channel_name'] = params['channel']
    context.user_data['date'] = params['date']
    context.user_data['time'] = params['time']
    context.user_data['output_file'] = params['filename']
    context.user_data['source'] = 'scheduled'
    
    return await show_audio_selection(update, context)


async def rec_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    /rec command for direct link recording
    Usage: /rec link 00:00:10
    """
    args = context.args
    
    if not args or len(args) < 2:
        await update.message.reply_text(
            "🔗 *Record from Link*\n\n"
            "Usage: `/rec <link> <duration>`\n\n"
            "Example:\n"
            "`/rec https://stream.url 00:00:10`",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    
    link = args[0]
    duration = args[1] if len(args) > 1 else "00:30:00"
    
    context.user_data['link'] = link
    context.user_data['duration'] = duration
    context.user_data['source'] = 'link'
    
    return await show_audio_selection(update, context)


async def setwatermarksize_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /setwatermarksize command
    Usage: /setwatermarksize 205
    """
    args = context.args
    
    if not args or not args[0].isdigit():
        await update.message.reply_text(
            "🖼 *Set Watermark Size*\n\n"
            "Usage: `/setwatermarksize <size>`\n\n"
            "Size range: 50-500 pixels\n"
            "Example: `/setwatermarksize 205`",
            parse_mode="Markdown"
        )
        return
    
    size = int(args[0])
    
    if 50 <= size <= 500:
        context.user_data['watermark_size'] = size
        await update.message.reply_text(
            f"✅ Watermark size set to *{size}px*",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ Size must be between 50 and 500 pixels"
        )


async def show_audio_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Step 1: Audio Track Selection"""
    
    keyboard = [
        [
            InlineKeyboardButton("☑️ Hindi", callback_data="audio_hindi"),
            InlineKeyboardButton("☐ Tamil", callback_data="audio_tamil"),
        ],
        [
            InlineKeyboardButton("☐ Telugu", callback_data="audio_telugu"),
            InlineKeyboardButton("☐ Kannada", callback_data="audio_kannada"),
        ],
        [
            InlineKeyboardButton("☐ English", callback_data="audio_english"),
        ],
        [
            InlineKeyboardButton("➡️ Next", callback_data="next_watermark"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = "🎧 *Step 1 — Audio Track*\n\nSelect your preferred audio language:"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            text=message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    return STEP_AUDIO


async def show_watermark_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Step 2: Watermark Position Selection"""
    
    keyboard = [
        [InlineKeyboardButton("↖️ Top Left", callback_data="watermark_top_left")],
        [InlineKeyboardButton("↗️ Top Right", callback_data="watermark_top_right")],
        [InlineKeyboardButton("🎯 Center", callback_data="watermark_center")],
        [InlineKeyboardButton("↙️ Bottom Left", callback_data="watermark_bottom_left")],
        [InlineKeyboardButton("↘️ Bottom Right", callback_data="watermark_bottom_right")],
        [InlineKeyboardButton("⬆️ Top Center", callback_data="watermark_top_center")],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back_audio"),
            InlineKeyboardButton("➡️ Next", callback_data="next_aspect"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = "🖼 *Step 2 — Watermark Position*\n\nSelect watermark placement:"
    
    await update.callback_query.edit_message_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return STEP_WATERMARK


async def show_aspect_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Step 3: Aspect Ratio Selection"""
    
    keyboard = [
        [InlineKeyboardButton("◉ 21:9 Aspect", callback_data="aspect_21:9")],
        [InlineKeyboardButton("○ 16:9 Aspect", callback_data="aspect_16:9")],
        [InlineKeyboardButton("○ 4:5 Aspect", callback_data="aspect_4:5")],
        [InlineKeyboardButton("○ 16:9 Black Bars", callback_data="aspect_16:9_black_bars")],
        [InlineKeyboardButton("○ 16:9 Zoom", callback_data="aspect_16:9_zoom")],
        [InlineKeyboardButton("○ Scale 1280×720", callback_data="aspect_1280x720")],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back_watermark"),
            InlineKeyboardButton("➡️ Next", callback_data="next_compression"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = "📺 *Step 3 — Aspect Ratio / Video Layout*\n\nChoose Video Layout:"
    
    await update.callback_query.edit_message_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return STEP_ASPECT


async def show_compression_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Step 4: Compression Selection"""
    
    keyboard = [
        [
            InlineKeyboardButton("⚡ Ultra Fast", callback_data="compression_ultrafast"),
            InlineKeyboardButton("🚀 Fast", callback_data="compression_fast"),
        ],
        [
            InlineKeyboardButton("⚖️ Medium", callback_data="compression_medium"),
            InlineKeyboardButton("🐌 Slow", callback_data="compression_slow"),
        ],
        [
            InlineKeyboardButton("📦 Skip", callback_data="compression_skip"),
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back_aspect"),
            InlineKeyboardButton("➡️ Next", callback_data="next_upload"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = "📦 *Step 4 — Compression*\n\nSelect compression method:"
    
    await update.callback_query.edit_message_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return STEP_COMPRESSION


async def show_upload_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Step 5: Upload Destination Selection"""
    
    keyboard = [
        [InlineKeyboardButton("💬 Telegram", callback_data="upload_telegram")],
        [InlineKeyboardButton("📁 Google Drive", callback_data="upload_drive")],
        [InlineKeyboardButton("🔄 Both", callback_data="upload_both")],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back_compression"),
            InlineKeyboardButton("✅ Start", callback_data="start_recording"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = "📤 *Step 5 — Upload Destination*\n\nSelect where to upload:"
    
    await update.callback_query.edit_message_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return STEP_UPLOAD


async def show_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show final recording summary"""
    
    user_data = context.user_data
    
    summary_text = (
        "🎬 *Recording Summary*\n\n"
        f"📺 Channel : {user_data.get('channel_name', 'Direct Link')}\n"
        f"⏰ Duration : {user_data.get('duration', 'N/A')}\n\n"
        f"🎧 Audio       : {user_data.get('audio', 'hindi').upper()}\n"
        f"🖼 Watermark   : {user_data.get('watermark', 'bottom_right').replace('_', ' ').title()}\n"
        f"📺 Layout      : {user_data.get('aspect', '16:9')}\n"
        f"📦 Compression : {user_data.get('compression', 'medium').replace('_', ' ').title()}\n"
        f"📤 Upload      : {user_data.get('upload', 'telegram').replace('_', ' ').title()}\n"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("▶️ Start", callback_data="confirm_start"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_recording"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        text=summary_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle all inline button callbacks"""
    
    query = update.callback_query
    await query.answer()
    
    # Audio selection
    if query.data.startswith("audio_"):
        audio = query.data.split("_", 1)[1]
        context.user_data['audio'] = audio
        return await show_watermark_selection(update, context)
    
    # Watermark selection
    elif query.data.startswith("watermark_"):
        watermark = query.data.split("_", 1)[1]
        context.user_data['watermark'] = watermark
        return await show_aspect_selection(update, context)
    
    # Aspect selection
    elif query.data.startswith("aspect_"):
        aspect = query.data.split("_", 1)[1]
        context.user_data['aspect'] = aspect
        return await show_compression_selection(update, context)
    
    # Compression selection
    elif query.data.startswith("compression_"):
        compression = query.data.split("_", 1)[1]
        context.user_data['compression'] = compression
        return await show_upload_selection(update, context)
    
    # Upload selection
    elif query.data.startswith("upload_"):
        upload = query.data.split("_", 1)[1]
        context.user_data['upload'] = upload
        return await show_summary(update, context)
    
    # Navigation
    elif query.data == "next_watermark":
        return await show_watermark_selection(update, context)
    elif query.data == "next_aspect":
        return await show_aspect_selection(update, context)
    elif query.data == "next_compression":
        return await show_compression_selection(update, context)
    elif query.data == "next_upload":
        return await show_upload_selection(update, context)
    
    elif query.data == "back_audio":
        return await show_audio_selection(update, context)
    elif query.data == "back_watermark":
        return await show_watermark_selection(update, context)
    elif query.data == "back_aspect":
        return await show_aspect_selection(update, context)
    elif query.data == "back_compression":
        return await show_compression_selection(update, context)
    
    elif query.data == "confirm_start":
        await query.edit_message_text(
            text="✅ *Recording Started!*\n\nYou will receive updates shortly.",
            parse_mode="Markdown"
        )
        logger.info(f"Recording started with config: {context.user_data}")
        return ConversationHandler.END
    
    elif query.data == "cancel_recording":
        await query.edit_message_text(
            text="❌ Recording cancelled.",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    
    return ConversationHandler.END
