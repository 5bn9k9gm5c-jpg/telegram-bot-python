import os
import sqlite3
import time

import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MY_TELEGRAM_ID = 464439065

DB_PATH = "bot.db"

bot = telebot.TeleBot(TOKEN)


def db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            max_price INTEGER,
            radius_km REAL,
            pets INTEGER DEFAULT 1,
            active INTEGER DEFAULT 1
        )
    """)

    connection.commit()
    connection.close()


def allowed(message):
    return message.from_user.id == MY_TELEGRAM_ID


def deny(message):
    if not allowed(message):
        return True
    return False


@bot.message_handler(commands=["start"])
def start(message):
    if deny(message):
        return

    bot.reply_to(
        message,
        "Привет 🤍\n\n"
        "Я бот для мониторинга квартир.\n\n"
        "Команды:\n"
        "/new — создать поиск\n"
        "/searches — мои поиски\n"
        "/pause — поставить мониторинг на паузу\n"
        "/resume — возобновить мониторинг\n"
        "/history — история\n"
        "/settings — настройки"
    )


@bot.message_handler(commands=["new"])
def new_search(message):
    if deny(message):
        return

    bot.reply_to(
        message,
        "Создадим поиск квартиры.\n\n"
        "Пока тестируем настройки.\n"
        "Напиши название поиска, например:\n\n"
        "Квартира Летний"
    )

    bot.register_next_step_handler(message, create_search)


def create_search(message):
    if deny(message):
        return

    name = message.text.strip()

    if not name:
        bot.reply_to(message, "Название не может быть пустым.")
        return

    connection = db()

    connection.execute(
        """
        INSERT INTO searches
        (user_id, name, city, max_price, radius_km, pets, active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            MY_TELEGRAM_ID,
            name,
            "Сочи",
            45000,
            2,
            1,
            1,
        ),
    )

    connection.commit()
    connection.close()

    bot.reply_to(
        message,
        f"Поиск «{name}» сохранён ✅\n\n"
        "Сейчас параметры:\n"
        "📍 Сочи\n"
        "💰 до 45 000 ₽\n"
        "📏 радиус до 2 км\n"
        "🐈 питомцы разрешены\n"
        "🏠 долгосрочная аренда"
    )


@bot.message_handler(commands=["searches"])
def searches(message):
    if deny(message):
        return

    connection = db()

    rows = connection.execute(
        """
        SELECT id, name, city, max_price, radius_km, pets, active
        FROM searches
        WHERE user_id = ?
        ORDER BY id
        """,
        (MY_TELEGRAM_ID,),
    ).fetchall
