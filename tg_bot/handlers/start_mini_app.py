from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from middlewares.role_middleware import requires_role
from typing import Union
from api.users import get_user, set_admin_role
from api.bookings import get_bookings_for_user
from aiogram import Router, F
from aiogram.types import Message
import logging

router = Router()
logger = logging.getLogger('SuperBot')

# Mini App URL - замените на ваш URL
MINI_APP_URL = "https://your-domain.com/frontend/index.html"

@router.message(Command("start"))
async def cmd_start(message: Message, **kwargs):
    telegram_id = message.from_user.id
    
    # Проверка авторизации
    is_authenticated, is_admin, user_name = await get_user(telegram_id)
    
    if is_authenticated:
        # Создаем клавиатуру с Mini App
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎯 Открыть приложение",
                        web_app=WebAppInfo(url=MINI_APP_URL)
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📋 Мои записи",
                        callback_data="user_bookings"
                    )
                ]
            ]
        )
        
        # Добавляем админ кнопку если пользователь админ
        if is_admin:
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text="⚙️ Админ панель",
                    callback_data="admin_panel"
                )
            ])
        
        await message.answer(
            f"Привет, {user_name}! 🎯\n\n"
            "Добро пожаловать в систему записи на тренировки!\n"
            "Нажмите кнопку ниже, чтобы открыть приложение:",
            reply_markup=keyboard
        )
    else:
        # Пользователь не зарегистрирован
        telegram_username = message.from_user.username
        await message.answer(
            f"Привет, {telegram_username}! 👋\n\n"
            "Для использования приложения необходимо зарегистрироваться.\n"
            "Пожалуйста, заполните данные:",
            reply_markup=get_register_keyboard()
        )

@router.message(Command("app"))
async def cmd_app(message: Message, **kwargs):
    """Команда для быстрого доступа к Mini App"""
    telegram_id = message.from_user.id
    is_authenticated, is_admin, user_name = await get_user(telegram_id)
    
    if not is_authenticated:
        await message.answer(
            "Для использования приложения необходимо зарегистрироваться.\n"
            "Используйте /start для регистрации."
        )
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

@router.callback_query(F.data == "open_app")
async def open_app_handler(query: CallbackQuery):
    """Обработчик кнопки открытия Mini App"""
    telegram_id = query.from_user.id
    is_authenticated, is_admin, user_name = await get_user(telegram_id)
    
    if not is_authenticated:
        await query.answer("Сначала зарегистрируйтесь!", show_alert=True)
        return
    
    # Открываем Mini App
    await query.answer()
    await query.message.answer(
        "Открываю приложение...",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎯 Открыть приложение",
                        web_app=WebAppInfo(url=MINI_APP_URL)
                    )
                ]
            ]
        )
    )

@router.callback_query(F.data == "test_admin")
async def test_admin_handler(query: CallbackQuery):
    """
    Хендлер нажатия на кнопку «Стать админом».
    """
    telegram_id = query.from_user.id

    # Вызываем API для назначения роли администратора
    response = await set_admin_role(telegram_id)
    if response.status_code != 200:
        await query.answer("Не удалось назначить админ-роль", show_alert=True)
        return

    # Парсим обновлённые данные пользователя из JSON-ответа
    updated_user = response.json()
    is_admin = updated_user.get("is_admin", False)

    # Создаем новую клавиатуру с Mini App
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎯 Открыть приложение",
                    web_app=WebAppInfo(url=MINI_APP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Мои записи",
                    callback_data="user_bookings"
                )
            ]
        ]
    )
    
    # Добавляем админ кнопку если пользователь админ
    if is_admin:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text="⚙️ Админ панель",
                callback_data="admin_panel"
            )
        ])

    # Редактируем клавиатуру в исходном сообщении
    await query.message.edit_reply_markup(reply_markup=keyboard)
    await query.answer("Роль админа назначена!")

@router.message(Command("admin"))
@router.callback_query(F.data == "admin_panel")
@requires_role("admin")
async def admin_command(event: Union[Message, CallbackQuery], **kwargs):
    """
    Хендлер команды /admin и нажатия на кнопку «Админ».
    """
    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer("Панель администратора доступна в Mini App")
    else:
        await event.answer("Панель администратора доступна в Mini App")

def get_register_keyboard():
    """Создает клавиатуру для регистрации"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Зарегистрироваться",
                    callback_data="register_user"
                )
            ]
        ]
    ) 