from datetime import date


class Event:
    """Событие, о котором нужно напомнить."""

    icon = "📅"
    kind = "event"

    def __init__(self, title, event_date, remind_days_before=1,
                 chat_id=None, event_id=None):
        self.title = title
        self.event_date = event_date          # объект datetime.date
        self.remind_days_before = remind_days_before
        self.chat_id = chat_id                # чей это бот-чат
        self.event_id = event_id              # номер события

    def to_dict(self):
        """Превращает событие в словарь, который можно записать в JSON."""
        return {
            "kind": self.kind,
            "title": self.title,
            "event_date": self.event_date.isoformat(),  # '2026-12-25'
            "remind_days_before": self.remind_days_before,
            "chat_id": self.chat_id,
            "event_id": self.event_id,
        }

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
    kind = "birthday"

    def describe(self):
        return f"{self.icon} День рождения: {self.title} — {self.event_date.strftime('%d.%m.%Y')}"


class Exam(Event):
    icon = "📝"
    kind = "exam"

    def describe(self):
        return f"{self.icon} Экзамен: {self.title} — {self.event_date.strftime('%d.%m.%Y')}"

EVENT_TYPES = {"event": Event, "birthday": Birthday, "exam": Exam}


def event_from_dict(data):
    """Создаёт событие нужного класса из словаря."""
    event_class = EVENT_TYPES.get(data["kind"], Event)
    return event_class(
        title=data["title"],
        event_date=date.fromisoformat(data["event_date"]),
        remind_days_before=data["remind_days_before"],
        chat_id=data["chat_id"],
        event_id=data["event_id"],
    )