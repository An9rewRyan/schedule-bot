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
        timeslot_service = TimeslotService(timeslot_repo=self.timeslot_repo, user_repo=self.user_repo)
        booking_date = datetime.strptime(booking_date, "%Y-%m-%d")
        start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        end_time = datetime.strptime(end_time, "%H:%M:%S").time()
        slots = await timeslot_service.get_free_slots(selected_date=booking_date, telegram_id=telegram_id,
                                                      start_time=start_time)
        start_minutes = start_time.hour * 60 + start_time.minute
        end_minutes = end_time.hour * 60 + end_time.minute
        requested_slots_amount = (end_minutes - start_minutes) // 30

        if requested_slots_amount < 3:
            raise BookingRequestException(
                "Booking duration is too short; at least 1.5 hours required."
            )
        if len(slots) < requested_slots_amount:
            raise BookingRequestException("Not enough available time slots for the chosen period.")
        booking_slots = []
        for slot in slots:
            if not booking_slots:
                booking_slots.append(slot)
            else:
                last_slot = booking_slots[-1]
                if last_slot.end_time == slot.start_time:
                    booking_slots.append(slot)
            if len(booking_slots) == requested_slots_amount:
                break

        if len(booking_slots) < requested_slots_amount:
            raise BookingRequestException("Requested consecutive slots are not available.")
        booking = Booking(
            user_id=user.id,
            start_time=start_time,
            end_time=end_time,
            date=booking_date,
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
