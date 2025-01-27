from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.db import User, TimeSlot
from fastapi import APIRouter
from src.models.schemas import UserCreate, UserAuth
from src.repository.db import get_async_session

app = FastAPI()
auth_router = APIRouter()


@auth_router.post("/authenticate", status_code=200)
async def check_user_auth(user_data: UserAuth, session: AsyncSession = Depends(get_async_session)):
    """
    Проверяет, зарегистрирован ли пользователь в базе данных по telegram_id.
    """
    result = await session.execute(select(User).where(User.telegram_id == user_data.telegram_id))
    user: User = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не аутентифицирован.",
        )
    return {"message": "Пользователь аутентифицирован", "user_name": user.first_name}


# POST запрос для регистрации пользователя
@auth_router.post("/register")
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    # Проверим, существует ли пользователь с таким telegram_id
    existing_user = await session.execute(select(User).where(User.telegram_id == user_data.telegram_id))
    existing_user = existing_user.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this Telegram ID already exists.")

    # Создание нового пользователя
    new_user = User(
        telegram_id=user_data.telegram_id,
        phone_number=user_data.phone_number,
        first_name=user_data.first_name,
        second_name=user_data.second_name,
        age=user_data.age,
    )

    # Добавляем нового пользователя в базу данных
    session.add(new_user)
    await session.commit()

    return {"message": "User successfully registered", "user": new_user}
