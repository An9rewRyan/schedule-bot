from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List


def get_user_bookings_keyboard(bookings: List[dict]) -> InlineKeyboardMarkup:
    keyboard = []

    for booking in bookings:
        booking_text = f"{booking['date']} | {booking['start_time']} - {booking['end_time']}"

        # Кнопка с информацией о бронировании
        keyboard.append([
            InlineKeyboardButton(
                text=booking_text,
                callback_data=f"BOOKING_{booking['id']}"
            )
        ])

        # Кнопки "Отменить" и "Перенести" под каждым бронированием
        keyboard.append([
            InlineKeyboardButton(
                text="❌ Отменить",
                callback_data=f"CANCEL_{booking['id']}"
            ),
            InlineKeyboardButton(
                text="🔄 Перенести",
                callback_data=f"RESCHEDULE_{booking['id']}"
            )
        ])

    # Кнопка "Назад" в конец списка
    keyboard.append([
        InlineKeyboardButton(text="⬅ Назад", callback_data="BACK_TO_MENU")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)