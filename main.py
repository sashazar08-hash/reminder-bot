import os

import telebot
from dotenv import load_dotenv

from bot.handlers import register_handlers
from core.storage import JsonStorage


def main():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Не найден BOT_TOKEN. Создай файл .env по образцу .env.example")
        return

    bot = telebot.TeleBot(token)
    storage = JsonStorage()
    register_handlers(bot, storage)

    print("Бот запущен. Остановить: Ctrl+C")
    bot.infinity_polling()


if __name__ == "__main__":
    main()