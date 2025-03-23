from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import time, date
from .booking_timeslot_link import BookingTimeSlotLink  # Это можно импортировать без цикла


class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # Связь с пользователем
    start_time: time
    end_time: time
    date: date

    time_slots: List["TimeSlot"] = Relationship(  # Аннотация строкой, но link_model передаём объектом
        back_populates="bookings", link_model=BookingTimeSlotLink
    )
