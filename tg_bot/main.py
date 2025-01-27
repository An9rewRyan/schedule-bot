import asyncio
import logging
from aiogram import Bot, Dispatcher
from middlewares.role_middleware import RoleMiddleware
from constants import BOT_TOKEN
from handlers import users_router, start_router, timeslots_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SuperBot')


# Инициализация маршрутизатора


async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(users_router)
    dp.include_router(timeslots_router)

    # Добавляем middleware для ролей
    USER_ROLES = {
        1147844769: "admin",
        # 987654321: "moderator",
        # 111222333: "user"
    }
    dp.update.outer_middleware(RoleMiddleware(USER_ROLES))

    # Запуск polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())