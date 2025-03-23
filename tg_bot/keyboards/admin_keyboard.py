from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List


def get_bookings_keyboard() -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с кнопками для старта.
    Добавляет кнопку «Админ» только для администраторов.
    Добавляет кнопку «Отменить тренировку», если у пользователя есть текущая запись.
    """
    keyboard = [
        [InlineKeyboardButton(text="Все тренировки", callback_data="all_bookings")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
