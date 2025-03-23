from fastapi import Depends, HTTPException, status
from src.models.db import User
from fastapi import APIRouter
from src.models.schemas import UserCreate, UserAuth
from src.api.dependencies import get_repository
from src.repository.crud import UserCRUDRepository
from src.services.user import UserService
from src.utilities.exceptions import UserNotFoundException, UserAlreadyAdminException

users_router = APIRouter()


@users_router.post("/authenticate", status_code=200)
async def check_user_auth(user_data: UserAuth,
                          user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository))):
    """
    Проверяет, зарегистрирован ли пользователь в базе данных по telegram_id.
    """
    user = await user_repo.get_user_by_telegram_id(telegram_id=user_data.telegram_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не аутентифицирован.",
        )
    return {"message": "Пользователь аутентифицирован", "user_name": user.first_name, "is_admin": user.is_admin}


@users_router.post("/register")
async def register_user(user_data: UserCreate,
                        user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository))):
    user = await user_repo.get_user_by_telegram_id(telegram_id=user_data.telegram_id)
    if user:
        raise HTTPException(status_code=400, detail="User with this Telegram ID already exists.")
    new_user = await user_repo.create_user(
        telegram_id=user_data.telegram_id,
        phone_number=user_data.phone_number,
        first_name=user_data.first_name,
        second_name=user_data.second_name,
        age=user_data.age,
    )
    return {"message": "User successfully registered", "user": new_user}


@users_router.patch("/users/{telegram_id}/admin", response_model=User)
async def add_admin_role(
        telegram_id: int,
        user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository))
):
    try:
        user_service = UserService(user_repo=user_repo)
        user = await user_service.assign_admin_role(telegram_id=telegram_id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не аутентифицирован.",
        )
    except UserAlreadyAdminException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже является админом",
        )
    return user
