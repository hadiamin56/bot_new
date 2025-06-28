from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
    CallbackQueryHandler
)

# Replace with your actual token
BOT_TOKEN = '8089308588:AAE08ICpqt7C2YDUaM7z0nkntqOUDc046No'

TARGET_CHAT_IDS = ['@Test_public56',
                   '@Test_public57']  # Add more as needed

# States
AWAITING_ANNOUNCEMENT = 1
AWAITING_CONFIRMATION = 2

# Store the announcement temporarily in user_data
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['📢 Send Announcement']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Welcome to the School Bot!\n\nChoose an option below:",
        reply_markup=reply_markup
    )

async def ask_for_announcement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Please type the announcement you want to send.")
    return AWAITING_ANNOUNCEMENT

async def preview_announcement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    context.user_data['announcement_text'] = text

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes, send", callback_data="confirm_send"),
         InlineKeyboardButton("❌ Cancel", callback_data="cancel_send")]
    ])

    await update.message.reply_text(
        f"📢 *Preview:*\n\n{text}\n\nDo you want to send this to all groups?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    return AWAITING_CONFIRMATION

async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_send":
        text = context.user_data.get('announcement_text')
        for chat_id in TARGET_CHAT_IDS:
            await context.bot.send_message(chat_id=chat_id, text=text)
        await query.edit_message_text("✅ Announcement sent to all groups/channels!")

    elif query.data == "cancel_send":
        await query.edit_message_text("❌ Announcement cancelled.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

# Main App
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^📢 Send Announcement$"), ask_for_announcement)
        ],
        states={
            AWAITING_ANNOUNCEMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, preview_announcement)
            ],
            AWAITING_CONFIRMATION: [
                CallbackQueryHandler(handle_confirmation)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("🚀 Bot is running...")
    app.run_polling()
