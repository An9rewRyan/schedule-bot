from pydantic import BaseModel
from datetime import time, date
from typing import List
from .timeslot import TimeSlotInfo


class UserBookingInfo(BaseModel):
    id: int
    date: date
    start_time: time
    end_time: time
    time_slots: List[TimeSlotInfo]

    class Config:
        orm_mode = True
        from_attributes=True

class BookingInfo(BaseModel):
    # booking_id: int
    date: str
    start_time: str
    end_time: str

    class Config:
        orm_mode = True
        from_attributes=True

