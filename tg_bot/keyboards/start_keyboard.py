from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List


def get_start_keyboard(is_admin: bool, telegram_id: int, user_bookings: List[dict] = []) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с кнопками для старта.
    Добавляет кнопку «Админ» только для администраторов.
    Добавляет кнопку «Отменить тренировку», если у пользователя есть текущая запись.
    """
    keyboard = [
        [InlineKeyboardButton(text="Записаться на тренировку", callback_data="choose_day")]
    ]

    if is_admin:
        # keyboard = []
        keyboard.append([InlineKeyboardButton(text="Админ", callback_data="admin_panel")])
    else:
        keyboard.append(([InlineKeyboardButton(text="Стать админом", callback_data="test_admin")]))

    if user_bookings:
        keyboard.append([InlineKeyboardButton(text="Мои тренировки", callback_data="user_bookings")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
