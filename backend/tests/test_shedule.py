import random
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TimeSlot:
    id: int
    start_time: datetime
    end_time: datetime
    visitors_amount: int


def generate_test_day(start_hour=8, end_hour=18, step_minutes=30):
    slots = []
    start_time = datetime.today().replace(hour=start_hour, minute=0, second=0, microsecond=0)
    end_time = start_time.replace(hour=end_hour)

    slot_id = 1
    while start_time < end_time:
        # Генерация количества посетителей с 20% шансом на создание свободного слота
        visitors_amount = random.randint(0, 2) if random.random() < 0.2 else random.randint(3, 4)

        slot = TimeSlot(
            id=slot_id,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=step_minutes),
            visitors_amount=visitors_amount
        )

        slots.append(slot)
        start_time += timedelta(minutes=step_minutes)
        slot_id += 1

    return slots


def find_free_periods(slots, min_slots=3):
    free_periods = []
    current_period = []

    for slot in slots:
        if slot.visitors_amount < 4:
            current_period.append(slot)
        else:
            if len(current_period) >= min_slots:
                free_periods.append(current_period)
            current_period = []  # Сброс при заполненном слоте

    # Проверка последнего накопленного периода
    if len(current_period) >= min_slots:
        free_periods.append(current_period)

    return free_periods


# Генерация тестового дня
test_slots = generate_test_day()

print("\nALL SLOTS\n")
for slot in test_slots:
    print(f"ID: {slot.id}, {slot.start_time.time()} - {slot.end_time.time()}, Visitors: {slot.visitors_amount}")

# Поиск свободных периодов
free_periods = find_free_periods(test_slots)

print("\nFREE PERIODS\n")
for period in free_periods:
    print(" --- ")
    for slot in period:
        print(f"ID: {slot.id}, {slot.start_time.time()} - {slot.end_time.time()}, Visitors: {slot.visitors_amount}")
