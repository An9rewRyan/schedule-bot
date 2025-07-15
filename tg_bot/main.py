import asyncio
import logging
from aiogram import Bot, Dispatcher
from middlewares.role_middleware import RoleMiddleware
from constants import BOT_TOKEN
from handlers import users_router, start_router, timeslots_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SuperBot')

# Добавляем детальное логирование для aiogram
aiogram_logger = logging.getLogger('aiogram')
aiogram_logger.setLevel(logging.INFO)


# Инициализация маршрутизатора


async def main():
    logger.info("🚀 Запуск Telegram бота...")
    
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    logger.info("📋 Регистрация роутеров...")
    dp.include_router(start_router)
    dp.include_router(users_router)
    dp.include_router(timeslots_router)

    # Добавляем middleware для ролей
    USER_ROLES = {
        1147844769: "admin",
        # 987654321: "moderator",
        # 111222333: "user"
    }
    # dp.update.outer_middleware(RoleMiddleware(USER_ROLES))
    
    logger.info("🔄 Начинаем polling...")
    logger.info("✅ Бот готов к получению сообщений!")

    # Запуск polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())