from pydantic import BaseModel
from datetime import datetime


class AvailableSlot(BaseModel):
    day: datetime
    start_time: datetime
    end_time: datetime
