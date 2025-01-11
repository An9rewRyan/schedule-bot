from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

times = [f"{hour}:00" for hour in range(11, 19)]


def get_times_keyboard(chosen_day: str) -> InlineKeyboardMarkup:
    """
    Создаём клавиатуру с интервалом времени (11:00 - 18:00).
    Callback_data вида TIME_Понедельник_11:00, и т.д.
    """
    keyboard = []
    for t in times:
        keyboard.append([
            InlineKeyboardButton(
                text=t,
                callback_data=f"TIME_{chosen_day}_{t}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
