from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = '8056779022:AAFi1QQjkjl-kLcPJ4rGzuXdQXyZhaZFHNg'

async def log_chat_id(update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    print(f"Chat Title: {chat.title} | ID: {chat.id}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, log_chat_id))
app.run_polling()
