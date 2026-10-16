from datetime import date

import pytest

from core.dates import parse_date
from core.exceptions import InvalidDateError
from core.models import Event

from core.storage import JsonStorage
from core.exceptions import EventNotFoundError

def test_parse_date_valid():
    assert parse_date("25.12.2026") == date(2026, 12, 25)

def test_parse_date_wrong_format():
    with pytest.raises(InvalidDateError):
        parse_date("2026-12-25")

def test_parse_date_nonexistent_date():
    with pytest.raises(InvalidDateError):
        parse_date("32.13.2026")

def test_should_remind_on_right_day():
    event = Event("Зачёт", date(2026, 12, 25), remind_days_before=1)
    assert event.should_remind(today=date(2026, 12, 24)) is True

def test_should_not_remind_too_early():
    event = Event("Зачёт", date(2026, 12, 25), remind_days_before=1)
    assert event.should_remind(today=date(2026, 12, 20)) is False

def test_storage_add_and_get(tmp_path):
    storage = JsonStorage(str(tmp_path / "data.json"))
    storage.add(Event("Зачёт", date(2026, 12, 25), chat_id=1))
    storage.add(Event("Чужое", date(2026, 12, 26), chat_id=2))

    events = storage.get_for_chat(1)
    assert len(events) == 1
    assert events[0].title == "Зачёт"


def test_storage_delete_missing_event(tmp_path):
    storage = JsonStorage(str(tmp_path / "data.json"))
    with pytest.raises(EventNotFoundError):
        storage.delete(chat_id=1, event_id=99)