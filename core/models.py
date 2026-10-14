from datetime import date


class Event:
    """Событие, о котором нужно напомнить."""

    icon = "📅"

    def __init__(self, title, event_date, remind_days_before=1,
                 chat_id=None, event_id=None):
        self.title = title
        self.event_date = event_date          # объект datetime.date
        self.remind_days_before = remind_days_before
        self.chat_id = chat_id                # чей это бот-чат
        self.event_id = event_id              # номер события

    def days_until(self, today=None):
        """Сколько дней осталось до события."""
        if today is None:
            today = date.today()
        return (self.event_date - today).days

    def should_remind(self, today=None):
        """Пора ли отправлять напоминание."""
        return self.days_until(today) == self.remind_days_before

    def describe(self):
        return f"{self.icon} {self.title} — {self.event_date.strftime('%d.%m.%Y')}"


class Birthday(Event):
    icon = "🎂"

    def describe(self):
        return f"{self.icon} День рождения: {self.title} — {self.event_date.strftime('%d.%m.%Y')}"


class Exam(Event):
    icon = "📝"

    def describe(self):
        return f"{self.icon} Экзамен: {self.title} — {self.event_date.strftime('%d.%m.%Y')}"