from datetime import date
from fastapi import APIRouter, Depends
from typing import List, Optional

from src.models.schemas import (
    UserBookingInfo,
    BookingInfo,
    UserId,
)
from src.api.dependencies import get_repository
from src.repository.crud import BookingCRUDRepository, TimeslotCRUDRepository, UserCRUDRepository
from src.services.booking import BookingService
from src.utilities.exceptions import UserNotFoundException, BookingNotFoundException, BookingRequestException
from fastapi import Depends, HTTPException, status

bookings_router = APIRouter()


@bookings_router.get("/bookings", response_model=List[UserBookingInfo])
async def get_bookings(
        telegram_id: Optional[int] = None,
        booking_date: Optional[date] = None,
        booking_repo: BookingCRUDRepository = Depends(get_repository(repo_type=BookingCRUDRepository))
):
    bookings = await booking_repo.get_bookings(telegram_id=telegram_id, booking_date=booking_date)
    return [UserBookingInfo.from_orm(booking) for booking in bookings]


@bookings_router.delete("/bookings")
async def delete_booking(
        booking_id: int,
        telegram_id: int,
        booking_repo: BookingCRUDRepository = Depends(get_repository(repo_type=BookingCRUDRepository)),
        timeslot_repo: TimeslotCRUDRepository = Depends(get_repository(repo_type=TimeslotCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository))
):
    # Создаем сервис с зависимостью от репозитория
    booking_service = BookingService(booking_repo=booking_repo, user_repo=user_repo, timeslot_repo=timeslot_repo)
    try:
        await booking_service.delete_booking(telegram_id, booking_id)
    except BookingNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Выбранная бронь не принадлежит пользователю, либо не существует",
        )
    return {"detail": "Booking deleted successfully"}


@bookings_router.post("/bookings")
async def create_booking(
        booking: BookingInfo,
        user: UserId,
        booking_repo: BookingCRUDRepository = Depends(get_repository(repo_type=BookingCRUDRepository)),
        timeslot_repo: TimeslotCRUDRepository = Depends(get_repository(repo_type=TimeslotCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository)),
):
    booking_service = BookingService(booking_repo=booking_repo, timeslot_repo=timeslot_repo, user_repo=user_repo)
    try:
        new_booking = await booking_service.create_booking(
            telegram_id=user.telegram_id,
            booking_date=booking.date,
            start_time=booking.start_time,
            end_time=booking.end_time
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не аутентифицирован.",
        )
    except BookingRequestException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании брони, {e.args[0]}",
        )
    return {
        "status": "success",
        "message": "Слоты успешно забронированы.",
        "booking_id": new_booking.id
    }
