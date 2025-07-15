from src.repository.db import engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

import asyncio
from src.models.db import User

from sqlmodel import select


async def get_async_session() -> AsyncSession:
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    session = async_session()  # Создаём сессию
    return session


async def create_test_user():
    session = await get_async_session()
    
    # Проверяем, существует ли уже пользователь с таким telegram_id
    statement = select(User).where(User.telegram_id == 123456)
    existing_user = await session.execute(statement)
    
    if existing_user.first() is None:
        # Создаем тестового пользователя
        test_user = User(
            telegram_id=123456,
            first_name="Test",
            second_name="User",
            age=25,
            phone_number="+1234567890",
            is_admin=False
        )
        
        session.add(test_user)
        await session.commit()
        print("Тестовый пользователь создан.")
    else:
        print("Тестовый пользователь уже существует.")

    await session.close()


# Запуск
if __name__ == "__main__":
    asyncio.run(create_test_user()) 