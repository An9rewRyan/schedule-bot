from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class BookingTimeSlotLink(SQLModel, table=True):
    booking_id: int = Field(foreign_key="booking.id", primary_key=True)
    time_slot_id: int = Field(foreign_key="timeslot.id", primary_key=True)