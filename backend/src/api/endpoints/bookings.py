from datetime import date
from fastapi import APIRouter, Depends, Response, Query
from typing import List, Optional
import logging

from backend.src.models.schemas import (
    UserBookingInfo,
    BookingInfo,
    UserId,
)
from backend.src.api.dependencies import get_repository
from backend.src.repository.crud import BookingCRUDRepository, TimeslotCRUDRepository, UserCRUDRepository
from backend.src.services.booking import BookingService
from backend.src.utilities.exceptions import UserNotFoundException, BookingNotFoundException, BookingRequestException
from fastapi import Depends, HTTPException, status

logger = logging.getLogger(__name__)

bookings_router = APIRouter()

logger.info("Bookings router initialized")

@bookings_router.options("/")
async def options_bookings(response: Response):
    """Handle CORS preflight requests for bookings endpoint"""
    logger.info("OPTIONS request to /api/bookings")
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"message": "OK"}

@bookings_router.options("/user/{telegram_id}")
async def options_user_bookings(response: Response, telegram_id: int):
    """Handle CORS preflight requests for user bookings endpoint"""
    logger.info(f"OPTIONS request to /api/bookings/user/{telegram_id}")
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"message": "OK"}

@bookings_router.get("/user/{telegram_id}", response_model=List[UserBookingInfo])
async def get_user_bookings(
        telegram_id: int,
        booking_repo: BookingCRUDRepository = Depends(get_repository(repo_type=BookingCRUDRepository))
):
    """Get bookings for a specific user by telegram_id"""
    logger.info(f"GET request to /api/bookings/user/{telegram_id}")
    bookings = await booking_repo.get_bookings(telegram_id=telegram_id, booking_date=None)
    return [UserBookingInfo.from_orm(booking) for booking in bookings]

@bookings_router.get("/", response_model=List[UserBookingInfo])
async def get_bookings(
        telegram_id: Optional[int] = Query(None, description="ID пользователя Telegram"),
        booking_date: Optional[date] = Query(None, description="Дата бронирования"),
        booking_repo: BookingCRUDRepository = Depends(get_repository(repo_type=BookingCRUDRepository))
):
    logger.info(f"GET request to /api/bookings with telegram_id={telegram_id}, booking_date={booking_date}")
    bookings = await booking_repo.get_bookings(telegram_id=telegram_id, booking_date=booking_date)
    return [UserBookingInfo.from_orm(booking) for booking in bookings]


@bookings_router.delete("/")
async def delete_booking(
        booking_id: int,
        telegram_id: int,
        booking_repo: BookingCRUDRepository = Depends(get_repository(repo_type=BookingCRUDRepository)),
        timeslot_repo: TimeslotCRUDRepository = Depends(get_repository(repo_type=TimeslotCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository))
):
    logger.info(f"DELETE request to /api/bookings with booking_id={booking_id}, telegram_id={telegram_id}")
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


@bookings_router.post("/")
async def create_booking(
        booking: BookingInfo,
        user: UserId,
        booking_repo: BookingCRUDRepository = Depends(get_repository(repo_type=BookingCRUDRepository)),
        timeslot_repo: TimeslotCRUDRepository = Depends(get_repository(repo_type=TimeslotCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository)),
):
    logger.info(f"POST request to /api/bookings")
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

logger.info("Bookings router endpoints registered")
