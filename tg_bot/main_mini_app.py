import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.types import Message
from middlewares.role_middleware import RoleMiddleware
from constants import BOT_TOKEN
from handlers import users_router, start_router, timeslots_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SuperBot')

# Mini App URL - замените на ваш URL
MINI_APP_URL = "https://your-domain.com/frontend/index.html"

async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Добавляем middleware для ролей
    USER_ROLES = {
        1147844769: "admin",
        # 987654321: "moderator",
        # 111222333: "user"
    }
    dp.update.outer_middleware(RoleMiddleware(USER_ROLES))

    # Регистрируем роутеры
    dp.include_router(start_router)
    dp.include_router(users_router)
    dp.include_router(timeslots_router)

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 