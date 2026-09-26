import os
import time
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

bot = telebot.TeleBot(TOKEN)


# ВРЕМЕННО: получаем Telegram ID владельца
@bot.message_handler(commands=["id"])
def get_id(message):
    bot.reply_to(
        message,
        f"Твой Telegram ID: {message.from_user.id}"
    )


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! 👋\n\n"
        "Я пока настраиваюсь.\n"
        "Чтобы получить твой Telegram ID, отправь команду /id"
    )


# Пока просто игнорируем всё остальное
@bot.message_handler(func=lambda message: True)
def ignore(message):
    pass


try:
    bot.delete_webhook(drop_pending_updates=True)
    bot.polling()

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    while True:
        time.sleep(3600)
