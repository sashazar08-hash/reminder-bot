from datetime import date

from telebot import types

from core.dates import parse_date, parse_days
from core.exceptions import (EventNotFoundError, InvalidDateError,
                             InvalidDaysError)
from core.models import EVENT_TYPES

HELP_TEXT = (
    "Я храню важные даты и напоминаю о них заранее.\n\n"
    "/add — добавить событие\n"
    "/list — показать мои события\n"
    "/delete НОМЕР — удалить событие\n"
    "/help — эта подсказка"
)

# Что пишет пользователь на кнопке -> ключ в EVENT_TYPES
KIND_LABELS = {
    "Событие": "event",
    "День рождения": "birthday",
    "Экзамен": "exam",
}


def register_handlers(bot, storage):
    """Подключает все обработчики команд к боту."""

    @bot.message_handler(commands=["start", "help"])
    def send_help(message):
        bot.send_message(message.chat.id, HELP_TEXT)

    @bot.message_handler(commands=["list"])
    def show_list(message):
        events = storage.get_for_chat(message.chat.id)
        if not events:
            bot.send_message(message.chat.id,
                             "Пока нет событий. Добавь первое: /add")
            return
        lines = [
            f"{e.event_id}. {e.describe()} "
            f"(напомню за {e.remind_days_before} дн.)"
            for e in events
        ]
        bot.send_message(message.chat.id, "\n".join(lines))

    @bot.message_handler(commands=["delete"])
    def delete_event(message):
        parts = message.text.split()
        if len(parts) != 2 or not parts[1].isdigit():
            bot.send_message(message.chat.id,
                             "Напиши номер события, например: /delete 3")
            return
        try:
            storage.delete(message.chat.id, int(parts[1]))
        except EventNotFoundError as err:
            bot.send_message(message.chat.id, str(err))
            return
        bot.send_message(message.chat.id, "Событие удалено.")

    # ---------- диалог /add: четыре шага ----------

    def is_cancelled(message):
        """Если пользователь отправил команду, диалог прерываем."""
        return message.text is not None and message.text.startswith("/")

    @bot.message_handler(commands=["add"])
    def ask_title(message):
        msg = bot.send_message(message.chat.id, "Как назвать событие?")
        bot.register_next_step_handler(msg, got_title)

    def got_title(message):
        if is_cancelled(message):
            bot.send_message(message.chat.id, "Добавление отменено.")
            return
        title = (message.text or "").strip()
        if not title:
            msg = bot.send_message(message.chat.id,
                                   "Нужен текст. Как назвать событие?")
            bot.register_next_step_handler(msg, got_title)
            return
        msg = bot.send_message(message.chat.id,
                               "Дата события в формате ДД.ММ.ГГГГ:")
        bot.register_next_step_handler(msg, got_date, title)

    def got_date(message, title):
        if is_cancelled(message):
            bot.send_message(message.chat.id, "Добавление отменено.")
            return
        try:
            event_date = parse_date(message.text or "")
            if event_date < date.today():
                raise InvalidDateError("Эта дата уже прошла. Введи будущую.")
        except InvalidDateError as err:
            msg = bot.send_message(message.chat.id, str(err))
            bot.register_next_step_handler(msg, got_date, title)
            return
        msg = bot.send_message(message.chat.id,
                               "За сколько дней напомнить? (0-30)")
        bot.register_next_step_handler(msg, got_days, title, event_date)

    def got_days(message, title, event_date):
        if is_cancelled(message):
            bot.send_message(message.chat.id, "Добавление отменено.")
            return
        try:
            days = parse_days(message.text or "")
        except InvalidDaysError as err:
            msg = bot.send_message(message.chat.id, str(err))
            bot.register_next_step_handler(msg, got_days, title, event_date)
            return
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                             one_time_keyboard=True)
        keyboard.add(*KIND_LABELS)
        msg = bot.send_message(message.chat.id, "Выбери тип события:",
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, got_kind, title, event_date, days)

    def got_kind(message, title, event_date, days):
        if is_cancelled(message):
            bot.send_message(message.chat.id, "Добавление отменено.",
                             reply_markup=types.ReplyKeyboardRemove())
            return
        if message.text not in KIND_LABELS:
            msg = bot.send_message(message.chat.id,
                                   "Выбери вариант с кнопки.")
            bot.register_next_step_handler(msg, got_kind, title,
                                           event_date, days)
            return
        event_class = EVENT_TYPES[KIND_LABELS[message.text]]
        event = event_class(title=title, event_date=event_date,
                            remind_days_before=days,
                            chat_id=message.chat.id)
        storage.add(event)
        bot.send_message(message.chat.id, f"Сохранено: {event.describe()}",
                         reply_markup=types.ReplyKeyboardRemove())