from sqlalchemy.future import select
from sqlmodel import select
from src.models.db import Booking, UserTimeSlotLink
from src.models.db.booking_timeslot_link import BookingTimeSlotLink
from src.repository.crud import BookingCRUDRepository, UserCRUDRepository, TimeslotCRUDRepository
from src.utilities.exceptions import (
    BookingNotFoundException,
    BookingRequestException,
    UserNotFoundException
)
from datetime import date, time, datetime
from .timeslot import TimeslotService


class BookingService:
    def __init__(self, booking_repo: BookingCRUDRepository, timeslot_repo: TimeslotCRUDRepository,
                 user_repo: UserCRUDRepository = None, ):
        self.booking_repo = booking_repo
        self.user_repo = user_repo
        self.timeslot_repo = timeslot_repo

    async def create_booking(
            self, telegram_id: int, booking_date: str, start_time: str, end_time: str
    ) -> Booking:
        user = await self.user_repo.get_user_by_telegram_id(telegram_id)
        if not user:
            raise UserNotFoundException
        
        # Преобразуем строки в нужные типы
        booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()
        
        # Получаем все доступные слоты для данной даты (без фильтрации по времени)
        all_slots = await self.timeslot_repo.get_timeslots_by_date(selected_date=booking_date_obj)
        
        # Фильтруем слоты, доступные для пользователя
        available_slots = []
        for slot in all_slots:
            if user not in slot.visitors and len(slot.visitors) < 4:
                available_slots.append(slot)
        
        # Сортируем по времени начала
        available_slots.sort(key=lambda x: x.start_time)
        
        # Находим последовательность слотов, начинающуюся с нужного времени
        booking_slots = []
        start_found = False
        
        for slot in available_slots:
            if slot.start_time == start_time_obj:
                start_found = True
                booking_slots.append(slot)
            elif start_found and booking_slots:
                # Проверяем, что слот идет сразу после предыдущего
                last_slot = booking_slots[-1]
                if last_slot.end_time == slot.start_time:
                    booking_slots.append(slot)
                    
                    # Проверяем, достигли ли мы нужного времени окончания
                    if slot.end_time >= end_time_obj:
                        break
                else:
                    # Пробел в слотах - останавливаемся
                    break
        
        if not start_found:
            raise BookingRequestException(f"No available slot found starting at {start_time}")
        
        # Проверяем, что у нас есть достаточно времени
        if not booking_slots:
            raise BookingRequestException("No consecutive slots available for the requested time")
        
        # Проверяем, что последний слот покрывает нужное время окончания
        last_slot = booking_slots[-1]
        if last_slot.end_time < end_time_obj:
            raise BookingRequestException("Requested consecutive slots are not available.")
        booking = Booking(
            user_id=user.id,
            start_time=start_time_obj,
            end_time=end_time_obj,
            date=booking_date_obj,
        )
        await self.booking_repo.add_booking(booking)
        booking_links = [
            BookingTimeSlotLink(booking_id=booking.id, time_slot_id=slot.id) for slot in booking_slots
        ]
        user_slot_links = [
            UserTimeSlotLink(user_id=user.id, time_slot_id=slot.id) for slot in booking_slots
        ]
        self.booking_repo.session.add_all(booking_links + user_slot_links)
        await self.booking_repo.commit()
        return booking

    async def delete_booking(self, telegram_id: int, booking_id: int) -> Booking:
        user = await self.user_repo.get_user_by_telegram_id(telegram_id)
        if not user:
            raise UserNotFoundException
        stmt = select(Booking).where(
            Booking.id == booking_id,
            Booking.user_id == user.id,
        )
        result = await self.booking_repo.session.execute(stmt)
        booking_obj = result.scalar_one_or_none()
        if not booking_obj:
            raise BookingNotFoundException("Booking not found or does not belong to the user.")
        await self.booking_repo.delete_booking(booking_obj)
        return booking_obj
