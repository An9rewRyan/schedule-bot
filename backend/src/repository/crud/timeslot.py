from sqlalchemy.future import select
from backend.src.models.db import TimeSlot
from datetime import date, time
from sqlalchemy.orm import selectinload
from sqlmodel import select
from typing import Optional
from .base import BaseCRUDRepository


class TimeslotCRUDRepository(BaseCRUDRepository):
    async def get_timeslots_by_date(self, selected_date: date, start_time: Optional[time] = None):
        query = (
            select(TimeSlot)
            .where(TimeSlot.date == selected_date)
            .options(selectinload(TimeSlot.visitors), selectinload(TimeSlot.bookings))
        )
        if start_time:
            query = query.where(TimeSlot.start_time >= start_time)
        query = query.order_by(TimeSlot.start_time)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_timeslots_by_date_range(self, start_date: date, end_date: date):
        """Получает таймслоты в диапазоне дат"""
        query = (
            select(TimeSlot)
            .where(TimeSlot.date >= start_date, TimeSlot.date <= end_date)
            .options(selectinload(TimeSlot.visitors), selectinload(TimeSlot.bookings))
            .order_by(TimeSlot.date, TimeSlot.start_time)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
