from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .user_timeslot_link import UserTimeSlotLink


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: Optional[int] = Field(index=True, unique=True)
    first_name: Optional[str] = Field(max_length=50)
    second_name: Optional[str] = Field(max_length=50)
    age: Optional[int] = Field()
    phone_number: Optional[str] = Field(max_length=13)
    time_slots: List["TimeSlot"] = Relationship(
        back_populates="visitors", link_model=UserTimeSlotLink
    )
