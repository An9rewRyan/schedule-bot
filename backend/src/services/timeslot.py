import logging

from backend.src.repository.crud.timeslot import TimeslotCRUDRepository
from backend.src.repository.crud.user import UserCRUDRepository
from datetime import date, time, timedelta
from typing import Optional, List
from backend.src.utilities.exceptions import UserNotFoundException


class TimeslotService:
    def __init__(self, timeslot_repo: TimeslotCRUDRepository, user_repo: UserCRUDRepository = None):
        self.user_repo = user_repo
        self.timeslot_repo = timeslot_repo

    async def get_free_slots(self, telegram_id: Optional[int] = None, selected_date: date = date.today(),
                             start_time: time = None):
        user = await self.user_repo.get_user_by_telegram_id(telegram_id=telegram_id)
        if not user:
            raise UserNotFoundException
        
        # Получаем все слоты на выбранную дату
        slots = await self.timeslot_repo.get_timeslots_by_date(selected_date=selected_date, start_time=start_time)
        # Фильтруем слоты, доступные для пользователя
        available_slots = []
        for slot in slots:
            if user not in slot.visitors and len(slot.visitors) < 4:
                available_slots.append(slot)
        # Сортируем по времени начала
        available_slots.sort(key=lambda x: x.start_time)
        
        # Фильтруем только те слоты, которые подходят для 90-минутных тренировок
        training_slots = []
        
        for i in range(len(available_slots) - 1):
            current_slot = available_slots[i]
            next_slot = available_slots[i + 1]
            
            # Проверяем, что текущий слот и следующий идут подряд
            if current_slot.end_time == next_slot.start_time:
                # Рассчитываем общую длительность двух слотов
                from datetime import datetime, timedelta
                start_time_obj = datetime.combine(selected_date, current_slot.start_time)
                end_time_obj = datetime.combine(selected_date, next_slot.end_time)
                duration_minutes = (end_time_obj - start_time_obj).total_seconds() / 60
                
                # Если есть минимум 90 минут, добавляем слот
                if duration_minutes >= 60:
                    training_slots.append(current_slot)
        return training_slots

    async def get_available_days(self, telegram_id: Optional[int] = None, days_ahead: int = 7) -> List[date]:
        """Получает список доступных дней для записи"""
        user = await self.user_repo.get_user_by_telegram_id(telegram_id=telegram_id)
        if not user:
            raise UserNotFoundException
        
        # Получаем таймслоты на ближайшие дни
        today = date.today()
        end_date = today + timedelta(days=days_ahead)
        
        # Получаем все таймслоты в диапазоне дат
        all_slots = await self.timeslot_repo.get_timeslots_by_date_range(start_date=today, end_date=end_date)
        
        # Группируем по датам и находим дни с доступными таймслотами
        available_days = set()
        for slot in all_slots:
            if user not in slot.visitors and len(slot.visitors) < 4:
                available_days.add(slot.date)
        
        return sorted(list(available_days))
