from typing import Optional
from sqlalchemy.future import select
from src.models.db import User, TimeSlot, Booking, UserTimeSlotLink
from src.models.db.booking_timeslot_link import BookingTimeSlotLink
from datetime import date, time
from sqlalchemy.orm import selectinload
from fastapi import status
from fastapi import HTTPException
from sqlmodel import select
from .base import BaseCRUDRepository
from src.utilities.exceptions import UserNotFoundException, BookingNotFoundException, TooSmallBookingDurationException, \
    NotEnoughSlotsException, BookingSaveFailedException, RequestedSlotsBusyException
from typing import List


class BookingCRUDRepository(BaseCRUDRepository):
    async def get_bookings(
            self,
            telegram_id: Optional[int] = None,
            booking_date: Optional[date] = None,
    ) -> List[Booking]:
        query = select(Booking).options(selectinload(Booking.time_slots))
        if telegram_id is not None:
            subquery = select(User.id).where(User.telegram_id == telegram_id)
            query = query.where(Booking.user_id == subquery)
        if booking_date is not None:
            query = query.where(Booking.date == booking_date)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add_booking(self, booking: Booking) -> None:
        self.session.add(booking)
        await self.session.flush()  # Обеспечивает заполнение booking.id

    async def commit(self) -> None:
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise BookingSaveFailedException(f"Error while saving booking: {str(e)}")

    async def delete_booking(self, booking: Booking) -> None:
        # Сначала удаляем все связи с таймслотами
        booking_links_stmt = select(BookingTimeSlotLink).where(BookingTimeSlotLink.booking_id == booking.id)
        booking_links_result = await self.session.execute(booking_links_stmt)
        booking_links = booking_links_result.scalars().all()
        
        # Удаляем связи booking-timeslot
        for link in booking_links:
            await self.session.delete(link)
        
        # Удаляем связи user-timeslot для этого бронирования
        user_links_stmt = select(UserTimeSlotLink).where(
            UserTimeSlotLink.user_id == booking.user_id,
            UserTimeSlotLink.time_slot_id.in_([link.time_slot_id for link in booking_links])
        )
        user_links_result = await self.session.execute(user_links_stmt)
        user_links = user_links_result.scalars().all()
        
        for link in user_links:
            await self.session.delete(link)
        
        # Теперь удаляем само бронирование
        await self.session.delete(booking)
        await self.session.commit()

    async def get_available_timeslots(
            self, booking_date: date, start_time: time, end_time: time, telegram_id: int
    ) -> List[TimeSlot]:
        statement = (
            select(TimeSlot)
            .where(
                TimeSlot.date == booking_date,
                TimeSlot.start_time >= start_time,
                ~TimeSlot.visitors.any(User.telegram_id == telegram_id),
            )
            .order_by(TimeSlot.start_time)
            .options(
                selectinload(TimeSlot.visitors),
                selectinload(TimeSlot.bookings),
            )
        )
        result = await self.session.execute(statement)
        return result.scalars().all()