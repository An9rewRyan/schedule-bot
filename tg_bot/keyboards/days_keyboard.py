from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


def get_days_keyboard() -> InlineKeyboardMarkup:
    """
    Создаём клавиатуру с днями недели.
    При нажатии на кнопку день уходит в callback_data вида DAY_Понедельник.
    """
    keyboard = []
    for day in days:
        keyboard.append([
            InlineKeyboardButton(
                text=day,
                callback_data=f"DAY_{day}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
