from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from magic_filter import F
from tg_bot.middlewares.role_middleware import requires_role
from typing import Union
from tg_bot.keyboards.days_keyboard import get_days_keyboard
from tg_bot.keyboards.time_keyboard import get_times_keyboard
from tg_bot.keyboards.start_keyboard import get_start_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, **kwargs):
    """
    Обработчик команды /start: бот предлагает выбрать день недели.
    """
    is_admin = kwargs.get("user_role") == "admin"
    await message.answer(
        "Привет! Выберите нужный вариант:",
        reply_markup=get_start_keyboard(is_admin)
    )


@router.callback_query(F.data == "choose_day")
async def choose_day_callback(callback: CallbackQuery):
    """
    Хендлер для callback-запроса на кнопку «Выбрать день».
    Отправляет клавиатуру с днями недели.
    """
    await callback.message.edit_text(
        "На какой день недели хотите записаться?",
        reply_markup=get_days_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("DAY_"))
async def day_chosen(callback: CallbackQuery):
    """
    Обработчик выбора дня.
    """
    user = callback.from_user
    user_id = user.id
    username = user.username
    full_name = f"{user.first_name} {user.last_name or ''}".strip()

    logger.info(f"Пользователь {full_name} (@{username}) с ID {user_id} выбрал день.")

    prefix, chosen_day = callback.data.split("_", maxsplit=1)
    await callback.message.edit_text(
        text=f"Вы выбрали день: {chosen_day}\nТеперь выберите время (11:00 - 18:00):",
        reply_markup=get_times_keyboard(chosen_day)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("TIME_"))
async def time_chosen(callback: CallbackQuery):
    """
    Срабатывает, когда пользователь выбрал время.
    Отправляем подтверждение записи.
    """
    prefix, chosen_day, chosen_time = callback.data.split("_", maxsplit=2)

    await callback.message.edit_text(
        text=(
            f"Вы записаны на тренировку:\n\n"
            f"День: {chosen_day}\n"
            f"Время: {chosen_time}"
        )
    )
    await callback.answer()


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
