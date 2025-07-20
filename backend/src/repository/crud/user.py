from sqlalchemy.future import select
from backend.src.models.db import User
from sqlmodel import select
from .base import BaseCRUDRepository
from backend.src.utilities.exceptions import UserNotFoundException
from backend.src.models.db import User


class UserCRUDRepository(BaseCRUDRepository):
    async def get_user_by_telegram_id(self, telegram_id: int) -> User:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        return user

    async def create_user(self, telegram_id: int, phone_number: str, first_name: str, second_name: str, age: int):
        new_user = User(
            telegram_id=telegram_id,
            phone_number=phone_number,
            first_name=first_name,
            second_name=second_name,
            age=age,
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def update_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

