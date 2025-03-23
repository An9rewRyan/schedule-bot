from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

def get_time_keyboard(start_times: List[dict], day: str) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с доступным временем для выбранного дня.
    :param start_times: Список доступного начального времени (например, ["09:00", "10:30"]).
    :param day: Выбранный день (например, "2025-01-24").
    :return: Клавиатура с кнопками для выбора времени.
    """
    keyboard = []
    for slot in start_times:
        keyboard.append([
            InlineKeyboardButton(
                text=slot['start_time'],  # Текст кнопки
                callback_data=f"TIME_{day}_{slot['start_time']}"  # Callback, содержащий дату и время
            )
        ])
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="BACK_TO_DAYS")])  # Кнопка "Назад"
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
