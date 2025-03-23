from sqlmodel import SQLModel, Field, Relationship
from datetime import date, time
from typing import List, Optional
from .booking_timeslot_link import BookingTimeSlotLink  # Можно импортировать без цикла
from .user_timeslot_link import UserTimeSlotLink  # Это тоже можно импортировать без цикла


class TimeSlot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start_time: time
    end_time: time
    date: date

    bookings: List["Booking"] = Relationship(  # Аннотация строкой, но link_model передаём объектом
        back_populates="time_slots", link_model=BookingTimeSlotLink
    )

    visitors: List["User"] = Relationship(
        back_populates="time_slots", link_model=UserTimeSlotLink
    )

    @property
    def is_available(self) -> bool:
        """Проверяет, есть ли свободные места в таймслоте (менее 4 посетителей)."""
        return len(self.visitors) < 4
