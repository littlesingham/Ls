"""
Upload command handlers for Telegram and Google Drive
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

logger = logging.getLogger(__name__)


async def handle_upload_complete(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                 file_path: str, upload_manager) -> None:
    """
    Handle post-recording upload options
    
    Args:
        update: Telegram update
        context: Telegram context
        file_path: Path to recorded file
        upload_manager: Upload manager instance
    """
    
    keyboard = [
        [
            InlineKeyboardButton("💬 Telegram", callback_data=f"upload_telegram_{file_path}"),
        ],
        [
            InlineKeyboardButton("📁 Google Drive", callback_data=f"upload_drive_{file_path}"),
        ],
        [
            InlineKeyboardButton("🔄 Both Telegram & Drive", callback_data=f"upload_both_{file_path}"),
        ],
        [
            InlineKeyboardButton("⏭️ Skip", callback_data="skip_upload"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "✅ *Recording Complete!*\n\n"
        f"📄 File: {file_path.split('/')[-1]}\n\n"
        "Where would you like to upload?"
    )
    
    await update.message.reply_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def upload_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE,
                         file_path: str, upload_manager) -> None:
    """Upload to Telegram"""
    
    query = update.callback_query
    await query.answer("🚀 Starting upload...")
    
    user_id = update.effective_user.id
    
    # Show progress update message
    progress_message = await query.edit_message_text(
        text="🚀 Resuming upload pipeline\n\n⏳ Initializing...",
        parse_mode="Markdown"
    )
    
    try:
        # Start upload
        results = await upload_manager.upload(
            user_id, file_path,
            destinations=['telegram']
        )
        
        if 'telegram' in results and results['telegram'] and results['telegram'] != 'Failed to upload':
            await progress_message.edit_text(
                text=(
                    "✅ *Sent*\n"
                    f"Task id: {list(upload_manager.active_uploads.keys())[-1]}\n\n"
                    "📹 Your recording has been uploaded to Telegram!"
                ),
                parse_mode="Markdown"
            )
        else:
            await progress_message.edit_text(
                text="❌ Upload failed",
                parse_mode="Markdown"
            )
    
    except Exception as e:
        logger.error(f"Error uploading: {e}")
        await progress_message.edit_text(
            text=f"❌ Error: {str(e)}",
            parse_mode="Markdown"
        )


async def upload_drive(update: Update, context: ContextTypes.DEFAULT_TYPE,
                      file_path: str, upload_manager) -> None:
    """Upload to Google Drive"""
    
    query = update.callback_query
    await query.answer("🚀 Starting upload...")
    
    # Show progress update message
    progress_message = await query.edit_message_text(
        text="🚀 Resuming upload pipeline\n\n⏳ Initializing...",
        parse_mode="Markdown"
    )
    
    try:
        # Start upload
        results = await upload_manager.upload(
            update.effective_user.id, file_path,
            destinations=['drive']
        )
        
        if 'drive' in results and results['drive'] and results['drive'] != 'Failed to upload':
            await progress_message.edit_text(
                text=(
                    "✅ *Sent*\n"
                    f"Task id: {list(upload_manager.active_uploads.keys())[-1]}\n\n"
                    "📁 Your recording has been uploaded to Google Drive!"
                ),
                parse_mode="Markdown"
            )
        else:
            await progress_message.edit_text(
                text="❌ Upload failed",
                parse_mode="Markdown"
            )
    
    except Exception as e:
        logger.error(f"Error uploading: {e}")
        await progress_message.edit_text(
            text=f"❌ Error: {str(e)}",
            parse_mode="Markdown"
        )


async def upload_both(update: Update, context: ContextTypes.DEFAULT_TYPE,
                     file_path: str, upload_manager) -> None:
    """Upload to both Telegram and Google Drive"""
    
    query = update.callback_query
    await query.answer("🚀 Starting uploads...")
    
    user_id = update.effective_user.id
    
    # Show progress update message
    progress_message = await query.edit_message_text(
        text="🚀 Resuming upload pipeline for Job a1\n\n⏳ Initializing...",
        parse_mode="Markdown"
    )
    
    try:
        # Start uploads
        results = await upload_manager.upload(
            user_id, file_path,
            destinations=['telegram', 'drive']
        )
        
        # Telegram upload
        telegram_status = "✅" if ('telegram' in results and results['telegram'] != 'Failed to upload') else "❌"
        telegram_task = list([k for k, v in upload_manager.active_uploads.items() 
                            if v.destination == 'telegram'])[-1] if [k for k, v in upload_manager.active_uploads.items() 
                                                                       if v.destination == 'telegram'] else "N/A"
        
        # Google Drive upload
        drive_status = "✅" if ('drive' in results and results['drive'] != 'Failed to upload') else "❌"
        drive_task = list([k for k, v in upload_manager.active_uploads.items() 
                          if v.destination == 'drive'])[-1] if [k for k, v in upload_manager.active_uploads.items() 
                                                                 if v.destination == 'drive'] else "N/A"
        
        message_text = (
            "🚀 *Upload Pipeline Complete*\n\n"
            f"🚀 Uploading to Telegram\n"
            f"📄 {file_path.split('/')[-1]}\n\n"
            f"┌ 📊 Upload Progress\n"
            f"├ [⬢⬢⬡⬡⬡⬡⬡⬡⬡⬡]  24.0%\n"
            f"├ 💾 Size  :    0.5 / 2.1 MB\n"
            f"└ 🆔 Task  : {telegram_task}\n\n"
            f"{telegram_status} Sent\nTask id: {telegram_task}\n\n"
            f"🚀 Uploading to Google Drive\n"
            f"📄 {file_path.split('/')[-1]}\n\n"
            f"┌ 📊 Upload Progress\n"
            f"├ [⬢⬢⬡⬡⬡⬡⬡⬡⬡⬡]  24.0%\n"
            f"├ 💾 Size  :    0.5 / 2.1 MB\n"
            f"└ 🆔 Task  : {drive_task}\n\n"
            f"{drive_status} Sent\nTask id: {drive_task}"
        )
        
        await progress_message.edit_text(
            text=message_text,
            parse_mode="Markdown"
        )
    
    except Exception as e:
        logger.error(f"Error uploading: {e}")
        await progress_message.edit_text(
            text=f"❌ Error: {str(e)}",
            parse_mode="Markdown"
        )


async def skip_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Skip upload"""
    
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="⏭️ Upload skipped. Your file is saved locally.",
        parse_mode="Markdown"
    )
