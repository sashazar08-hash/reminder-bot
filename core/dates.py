from datetime import datetime

from core.exceptions import InvalidDateError, InvalidDaysError

MAX_REMIND_DAYS = 30

DATE_FORMAT = "%d.%m.%Y"

def parse_date(text):
    """Превращает строку вида '25.12.2026' в объект date.

        Если строка неверная, выбрасывает InvalidDateError.
    """
    try:
        return datetime.strptime(text.strip(), DATE_FORMAT).date()
    except ValueError:
        raise InvalidDateError(
            "Не удалось разобрать дату. Введите ее в формате ДД.ММ.ГГГГ, "
            "например 25.12.2026"
        ) from None

def parse_days(text):
    """Превращает '3' в число 3. Разрешены числа от 0 до 30."""
    try:
        days = int(text.strip())
    except ValueError:
        raise InvalidDaysError("Нужно целое число, например 1 или 3.") from None
    if not 0 <= days <= MAX_REMIND_DAYS:
        raise InvalidDaysError(
            f"Число дней должно быть от 0 до {MAX_REMIND_DAYS}."
        )
    return days