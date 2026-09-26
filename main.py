import os
import time
import telebot
from dotenv import load_dotenv
from commands import register_commands

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

try:
    bot = telebot.TeleBot(TOKEN)
    register_commands(bot)

    @bot.message_handler(commands=["id"])
    def send_id(message):
        bot.reply_to(message, f"Твой Telegram ID: {message.from_user.id}")

    @bot.message_handler(commands=["start", "hello"])
    def send_welcome(message):
        bot.reply_to(message, "Hello! I'm a simple Telegram bot.")

    bot.delete_webhook(drop_pending_updates=True)
    bot.polling()

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    while True:
        time.sleep(3600)
