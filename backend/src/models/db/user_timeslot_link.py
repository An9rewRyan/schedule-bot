from sqlmodel import SQLModel, Field


class UserTimeSlotLink(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    time_slot_id: int = Field(foreign_key="timeslot.id", primary_key=True)
