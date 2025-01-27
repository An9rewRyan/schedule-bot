from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
from typing import List

def get_days_keyboard(available_days: List[str]) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с доступными днями.
    :param available_days: список доступных дней (например, ["2025-01-23", "2025-01-24"]).
    :return: клавиатура с кнопками для выбора дня.
    """
    keyboard = []
    for day in available_days:
        keyboard.append([
            InlineKeyboardButton(
                text=day,  # Текст кнопки
                callback_data=f"DAY_{day}"  # Callback, который отправляется при нажатии
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)