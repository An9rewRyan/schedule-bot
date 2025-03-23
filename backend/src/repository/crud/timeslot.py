from sqlalchemy.future import select
from src.models.db import TimeSlot
from datetime import date, time
from sqlalchemy.orm import selectinload
from sqlmodel import select
from .base import BaseCRUDRepository


class TimeslotCRUDRepository(BaseCRUDRepository):
    async def get_timeslots_by_date(self, selected_date: date, start_time: time = None):
        query = (
            select(TimeSlot)
            .where(TimeSlot.date == selected_date)
            .options(selectinload(TimeSlot.visitors), selectinload(TimeSlot.bookings))
        )
        if start_time:
            query = query.where(TimeSlot.start_time >= start_time).order_by(TimeSlot.start_time)
        result = await self.session.execute(query)
        return result.scalars().all()
