from aiogram.types import TelegramObject
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from functools import wraps
from aiogram.types import Message, CallbackQuery, Update
from typing import Callable, Union
import logging
logger = logging.getLogger('role-middleware')
logging.basicConfig(level=logging.INFO)


class RoleMiddleware(BaseMiddleware):
    def __init__(self, user_roles: dict):
        super().__init__()
        self.user_roles = user_roles

    async def __call__(self, handler, event: TelegramObject, data: dict):
        # Извлечение user_id из объекта Update
        if isinstance(event, Update):
            if event.message:
                user_id = event.message.from_user.id
            elif event.callback_query:
                user_id = event.callback_query.from_user.id
            else:
                logger.info('Обработка не поддерживается, возвращаем хендлер')
                return await handler(event, data)
        elif isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
        else:
            logger.info('Обработка не поддерживается, возвращаем хендлер')
            return await handler(event, data)

        # Получаем роль пользователя (по умолчанию "guest")
        user_role = self.user_roles.get(user_id, "guest")
        data["user_role"] = user_role  # Передаём роль в обработчик
        logger.info(f"User ID: {user_id}, Role: {user_role}")
        return await handler(event, data)


def requires_role(required_role: str):
    def decorator(handler: Callable):
        @wraps(handler)
        async def wrapper(event: Union[Message, CallbackQuery], **kwargs):
            user_role = kwargs.get("user_role", "guest")  # Извлекаем роль из kwargs
            if user_role != required_role:
                if isinstance(event, Message):
                    await event.answer("У вас нет доступа к этой команде.")
                elif isinstance(event, CallbackQuery):
                    await event.answer("У вас нет доступа.")
                return
            return await handler(event, **kwargs)

        return wrapper

    return decorator
