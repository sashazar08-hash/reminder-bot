import json
import os

from core.exceptions import EventNotFoundError
from core.models import event_from_dict


class Storage:
    """Базовый класс хранилища. Описывает, какие методы должны быть."""

    def add(self, event):
        raise NotImplementedError

    def get_for_chat(self, chat_id):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def delete(self, chat_id, event_id):
        raise NotImplementedError


class JsonStorage(Storage):
    """Хранит события в JSON-файле."""

    def __init__(self, path="data.json"):
        self.path = path
        self._events = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, encoding="utf-8") as file:
                return [event_from_dict(item) for item in json.load(file)]
        except (json.JSONDecodeError, KeyError, ValueError):
            return []   # файл повреждён: начинаем с пустого списка

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump([e.to_dict() for e in self._events], file,
                      ensure_ascii=False, indent=2)

    def _next_id(self):
        return max((e.event_id for e in self._events), default=0) + 1

    def add(self, event):
        event.event_id = self._next_id()
        self._events.append(event)
        self._save()
        return event

    def get_for_chat(self, chat_id):
        events = [e for e in self._events if e.chat_id == chat_id]
        return sorted(events, key=lambda e: e.event_date)

    def get_all(self):
        return list(self._events)

    def delete(self, chat_id, event_id):
        for event in self._events:
            if event.event_id == event_id and event.chat_id == chat_id:
                self._events.remove(event)
                self._save()
                return
        raise EventNotFoundError(f"Событие с номером {event_id} не найдено.")