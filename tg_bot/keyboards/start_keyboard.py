from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_keyboard(is_admin: bool, telegram_id: int) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с кнопками для старта.
    Добавляет кнопку «Админ» только для администраторов.
    """

    keyboard = [[InlineKeyboardButton(text="Записаться на тренировку", callback_data="choose_day")]]

    if is_admin:
        keyboard.append([InlineKeyboardButton(text="Админ", callback_data="admin_panel")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
