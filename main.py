import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Отримуємо токен з Railway Variables
TOKEN = os.getenv("TOKEN")

# URL Google Apps Script
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyGjP6QCkmtFN18etI5OlkA-3Mz3JCTzsKtQcstA56II90m4frblM7BU1VApv0vVpN1/exec"

logging.basicConfig(level=logging.INFO)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Вітаю! Це Скринька довіри.\n"
        "Напишіть будь-яке повідомлення — воно буде збережене анонімно."
    )

# Обробка повідомлень
async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message = update.message.text

    data = {
        "user_id": user.id,
        "name": user.first_name,
        "message": message
    }

    try:
        requests.post(SCRIPT_URL, json=data)
        await update.message.reply_text("✅ Ваше повідомлення збережене.")
    except:
        await update.message.reply_text("⚠️ Помилка з’єднання. Спробуйте пізніше.")

# Головна функція
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message))

    app.run_polling()

if __name__ == "__main__":
    main()
