class ReminderBotError(Exception):
    """Базовая ошибка проекта. От неё наследуются все остальные."""


class InvalidDateError(ReminderBotError):
    """Пользователь ввёл дату в неверном формате или несуществующую дату."""


class EventNotFoundError(ReminderBotError):
    """Событие с таким номером не найдено."""