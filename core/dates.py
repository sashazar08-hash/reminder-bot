from datetime import datetime

from core.exceptions import  InvalidDateError

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