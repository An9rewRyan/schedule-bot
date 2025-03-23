from datetime import date
from backend.src.services import TimeslotService
from backend.src.repository.crud import TimeslotCRUDRepository
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter
from src.api.dependencies import get_repository
from src.repository.crud import UserCRUDRepository
from src.utilities.exceptions import UserNotFoundException, TooSmallBookingDurationException
from src.models.schemas import TimeSlotInfoVisitors
from src.models.db import TimeSlot
timeslots_router = APIRouter()


@timeslots_router.get("/slots")
async def get_available_slots(
        telegram_id: int = None,
        selected_date: date = date.today(),
        user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository)),
        timeslot_repo: TimeslotCRUDRepository = Depends(get_repository(repo_type=TimeslotCRUDRepository))
):
    free_slots = []
    timeslot_service = TimeslotService(user_repo=user_repo, timeslot_repo=timeslot_repo)
    try:
        free_slots = await timeslot_service.get_free_slots(telegram_id=telegram_id, selected_date=selected_date)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не аутентифицирован.",
        )
    except Exception as e:
        a = 1

    return {"available_periods": [TimeSlotInfoVisitors.from_orm(slot) for slot in free_slots]}
