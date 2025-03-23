from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from tg_bot.middlewares.role_middleware import requires_role
from typing import Union
from tg_bot.keyboards.days_keyboard import get_days_keyboard
from tg_bot.keyboards.time_keyboard import get_time_keyboard
from tg_bot.keyboards.start_keyboard import get_start_keyboard
from tg_bot.keyboards.register_keyboard import get_register_keyboard
from tg_bot.keyboards.admin_keyboard import get_bookings_keyboard
from tg_bot.api.timeslots import get_free_days, get_available_slots
from tg_bot.api.bookings import book_slots, get_bookings_for_user
from tg_bot.api.users import set_admin_role
from tg_bot.helpers import *
from tg_bot.api.users import get_user
from aiogram import Router, F
from aiogram.types import Message
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import httpx

router = Router()

logger = logging.getLogger('SuperBot')


@router.message(Command("start"))
async def cmd_start(message: Message, **kwargs):
    telegram_id = message.from_user.id
    # Проверка авторизации
    is_authenticated, is_admin, user_name = await get_user(telegram_id)
    if is_authenticated:
        user_bookings = await get_bookings_for_user(telegram_id)
        await message.answer(
            f"Привет, {user_name}, пора пострелять!",
            reply_markup=get_start_keyboard(is_admin=is_admin, telegram_id=telegram_id, user_bookings=user_bookings)
        )
    else:
        telegram_username = message.from_user.username
        await message.answer(
            f"Привет, {telegram_username}! Чтобы записаться, заполните данные:",
            reply_markup=get_register_keyboard()
        )


@router.callback_query(F.data == "test_admin")
async def test_admin_handler(query: CallbackQuery):
    """
    Хендлер нажатия на кнопку «Стать админом».
    Вызывает API для назначения роли админа, получает обновлённые данные пользователя,
    генерирует новую клавиатуру и обновляет сообщение.
    """
    telegram_id = query.from_user.id  # Получаем telegram_id из данных пользователя

    # Вызываем API для назначения роли администратора
    response = await set_admin_role(telegram_id)
    if response.status_code != 200:
        await query.answer("Не удалось назначить админ-роль", show_alert=True)
        return

    # Парсим обновлённые данные пользователя из JSON-ответа
    updated_user = response.json()
    is_admin = updated_user.get("is_admin", False)

    # Генерируем новую клавиатуру с учётом обновлённого флага is_admin
    new_keyboard = get_start_keyboard(is_admin, telegram_id)

    # Редактируем клавиатуру в исходном сообщении
    await query.message.edit_reply_markup(reply_markup=new_keyboard)
    await query.answer("Роль админа назначена!")


@router.message(Command("admin"))
@router.callback_query(F.data == "admin_panel")
@requires_role("admin")
async def admin_command(event: Union[Message, CallbackQuery], **kwargs):
    """
    Хендлер команды /admin и нажатия на кнопку «Админ».
    """
    await event.answer("Все тренировки")
