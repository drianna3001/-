import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Ваш токен від BotFather
TOKEN = "8333620769:AAHqpH9tx1pkwW-BnkPsDdVbtXNJTk3Ssu0"
# 🌐 URL Google Apps Script
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyGjP6QCkmtFN18etI5OlkA-3Mz3JCTzsKtQcstA56II90m4frblM7BU1VApv0vVpN1/exec"

logging.basicConfig(level=logging.INFO)

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Вітаю! Це Скринька довіри.\n"
        "Ви можете написати сюди будь-що, що вас турбує.\n"
        "Ваше повідомлення буде збережене анонімно у шкільній системі."
    )

# Отримання повідомлень
async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message = update.message.text

    # Відправляємо в Google Таблицю
    data = {
        "user_id": user.id,
        "name": user.first_name,
        "message": message
    }
    try:
        requests.post(SCRIPT_URL, json=data)
        await update.message.reply_text("✅ Ваше повідомлення успішно збережене!")
    except:
        await update.message.reply_text("⚠️ Помилка з’єднання. Спробуйте пізніше.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message))
    app.run_polling()

if __name__ == "__main__":
    main()
