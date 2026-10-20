import threading
import time
from datetime import date

CHECK_INTERVAL = 60  # проверять раз в минуту


class ReminderService:
    """Фоновая проверка: пора ли отправить напоминания."""

    def __init__(self, bot, storage):
        self.bot = bot
        self.storage = storage
        self._sent = set()   # пары (event_id, дата), чтобы не слать дважды

    def check_once(self, today=None):
        """Одна проверка: отправляет все напоминания, которые пора слать."""
        if today is None:
            today = date.today()
        for event in self.storage.get_all():
            key = (event, today)
            if key in self._sent:
                continue
            if event.should_remind(today):
                self._send(event, today)
                self._sent.add(key)

    def _send(self, event, today):
        days = event.days_until(today)
        if days == 0:
            when = "сегодня"
        elif days == 1:
            when = "завтра"
        else:
            when = f"через {days} дн."
        text = f"🔔 Напоминание ({when}):\n{event.describe()}"
        try:
            self.bot.send_message(event.chat_id, text)
        except Exception as err:
            print(f"Не удалось отправить напоминание: {err}")

    def _run(self):
        while True:
            self.check_once()
            time.sleep(CHECK_INTERVAL)

    def start(self):
        """Запускает проверку в фоновом потоке."""
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()