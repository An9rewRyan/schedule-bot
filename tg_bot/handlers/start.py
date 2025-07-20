from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
import logging

# Mini App URL - используем наш ngrok URL для frontend
MINI_APP_URL = "https://61786e357727.ngrok-free.app"

router = Router()

logger = logging.getLogger('SuperBot')


@router.message(Command("start"))
async def cmd_start(message: Message, **kwargs):
    if not message.from_user:
        return
    telegram_id = message.from_user.id
    logger.info(f"🎯 Получена команда /start от пользователя {telegram_id}")
    
    # Создаем простую клавиатуру только с Mini App
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎯 Открыть приложение",
                    web_app=WebAppInfo(url=MINI_APP_URL)
                )
            ]
        ]
    )
    
    await message.answer(
        f"Привет! 🎯\n\n"
        "Добро пожаловать в систему записи на тренировки!\n"
        "Нажмите кнопку ниже, чтобы открыть приложение:",
        reply_markup=keyboard
    )


@router.message(Command("app"))
async def cmd_app(message: Message, **kwargs):
    """Команда для быстрого доступа к Mini App"""
    if not message.from_user:
        return
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎯 Открыть приложение",
                    web_app=WebAppInfo(url=MINI_APP_URL)
                )
            ]
        ]
    )
    
    await message.answer(
        "Открываю приложение для записи на тренировки...",
        reply_markup=keyboard
    )



