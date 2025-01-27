from pydantic import BaseModel
from datetime import time, date
from typing import List


class UserSlotInfo(BaseModel):
    user_id: int


class OccupiedSlotInfo(BaseModel):
    start_time: time
    end_time: time
    date: date
    users: List[UserSlotInfo]
