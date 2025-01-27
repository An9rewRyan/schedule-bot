from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from tg_bot.middlewares.role_middleware import requires_role
from typing import Union
from tg_bot.keyboards.days_keyboard import get_days_keyboard
from tg_bot.keyboards.time_keyboard import get_time_keyboard
from tg_bot.keyboards.start_keyboard import get_start_keyboard
from tg_bot.keyboards.register_keyboard import get_register_keyboard
from tg_bot.api.timeslots import get_free_days, get_available_slots, book_slots
from tg_bot.helpers import *
from tg_bot.api.users import get_user
from aiogram import Router, F
from aiogram.types import Message

router = Router()

logger = logging.getLogger('SuperBot')


@router.message(Command("start"))
async def cmd_start(message: Message, **kwargs):
    telegram_id = message.from_user.id
    # Проверка авторизации
    is_authenticated, user_name = await get_user(telegram_id)
    if is_authenticated:
        await message.answer(
            f"Привет, {user_name}, пора пострелять!",
            reply_markup=get_start_keyboard(is_admin=False, telegram_id=telegram_id)
        )
    else:
        telegram_username = message.from_user.username
        await message.answer(
            f"Привет, {telegram_username}! Чтобы записаться, заполните данные:",
            reply_markup=get_register_keyboard()
        )


@router.message(Command("admin"))
@router.callback_query(F.data == "admin_panel")
@requires_role("admin")
async def admin_command(event: Union[Message, CallbackQuery], **kwargs):
    """
    Хендлер команды /admin и нажатия на кнопку «Админ».
    """
    if isinstance(event, Message):
        await event.answer("Добро пожаловать в панель администратора!")
    elif isinstance(event, CallbackQuery):
        await event.message.edit_text("Добро пожаловать в панель администратора!")
        await event.answer()
