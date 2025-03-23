from src.repository.crud.timeslot import TimeslotCRUDRepository
from src.repository.crud.user import UserCRUDRepository
from datetime import date, time
from src.utilities.exceptions import UserNotFoundException


class TimeslotService:
    def __init__(self, timeslot_repo: TimeslotCRUDRepository, user_repo: UserCRUDRepository = None):
        self.user_repo = user_repo
        self.timeslot_repo = timeslot_repo

    async def get_free_slots(self, telegram_id: int = None, selected_date: date = date.today(),
                             start_time: time = None):
        user = await self.user_repo.get_user_by_telegram_id(telegram_id=telegram_id)
        if not user:
            raise UserNotFoundException
        slots = await self.timeslot_repo.get_timeslots_by_date(selected_date=selected_date, start_time=start_time)
        user_not_taken_slots = []
        good_start_times = []
        slots_strike = []
        for slot in slots:
            if user not in slot.visitors and len(slot.visitors) < 4:
                user_not_taken_slots.append(slot)
        for i in range(len(user_not_taken_slots) - 1):
            if len(slots_strike) == 3:
                good_start_times.append(slots_strike.pop(0))
            if user_not_taken_slots[i].end_time == user_not_taken_slots[i + 1].start_time:
                slots_strike.append(user_not_taken_slots[i])
            else:
                if user_not_taken_slots[i].start_time == user_not_taken_slots[i - 1].end_time and len(
                        slots_strike) == 2:
                    user_not_taken_slots.append(slots_strike.pop(0))
                slots_strike = []

        return user_not_taken_slots
