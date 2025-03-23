from src.repository.crud.timeslot import TimeslotCRUDRepository
from src.repository.crud.user import UserCRUDRepository
from datetime import date
from src.utilities.exceptions import UserNotFoundException, UserAlreadyAdminException


class UserService:
    def __init__(self, user_repo: UserCRUDRepository = None):
        self.user_repo = user_repo

    async def assign_admin_role(self, telegram_id: int):
        user = await self.user_repo.get_user_by_telegram_id(telegram_id=telegram_id)
        if not user:
            raise UserNotFoundException
        elif user.is_admin:
            raise UserAlreadyAdminException
        user.is_admin = True
        user = self.user_repo.update_user(user=user)
        return user
