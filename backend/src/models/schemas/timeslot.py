from pydantic import BaseModel
from datetime import time, date
from typing import List


class UserSlotInfo(BaseModel):
    telegram_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class OccupiedSlotInfo(BaseModel):
    start_time: time
    end_time: time
    date: date
    users: List[UserSlotInfo]


class UserSlotsInfo(BaseModel):
    start_time: time
    end_time: time
    date: date


class TimeSlotInfo(BaseModel):
    id: int
    start_time: time
    end_time: time
    date: date

    class Config:
        orm_mode = True
        from_attributes = True


class TimeSlotInfoVisitors(BaseModel):
    id: int
    start_time: time
    end_time: time
    date: date
    visitors: List[UserSlotInfo]

    class Config:
        orm_mode = True
        from_attributes = True

# class UserSlotInfoFull(BaseModel):
#     telegram_id: int
#     first_name: str
#     second_name: str
#     phone_number: str
#     age: int
