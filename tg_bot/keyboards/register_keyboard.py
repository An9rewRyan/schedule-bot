from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_register_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Начать регистрацию")]
        ],
        resize_keyboard=True
    )


def get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отмена")]
        ],
        resize_keyboard=True
    )


def get_confirmation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Подтвердить"), KeyboardButton(text="Изменить")]
        ],
        resize_keyboard=True
    )
