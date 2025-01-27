import logging
from aiogram import Router
from typing import List, Dict

def extract_start_times_for_training(slots: List[Dict]) -> List[str]:
    """
    Извлекает времена, которые могут быть началом тренировки.
    :param slots: Список временных промежутков из API (формат как в get_available_slots).
    :return: Список начальных времён, подходящих для тренировки.
    """
    valid_start_times = []

    for period in slots:
        slot_ids = period["slot_ids"]
        start_time = period["start_time"]
        end_time = period["end_time"]

        # Генерируем список всех временных слотов в данном периоде
        all_start_times = generate_start_times(start_time, len(slot_ids), slot_duration=30)

        # Проверяем каждое время на возможность начала тренировки
        for i in range(len(all_start_times) - 2):  # -2, чтобы оставить место для двух последующих слотов
            valid_start_times.append(all_start_times[i])

    return valid_start_times


def generate_start_times(start_time: str, num_slots: int, slot_duration: int = 30) -> List[str]:
    """
    Генерирует список всех временных интервалов в периоде.
    :param start_time: Начальное время периода (например, '08:00:00').
    :param num_slots: Количество доступных слотов.
    :param slot_duration: Длительность одного слота в минутах.
    :return: Список времён в формате 'HH:MM'.
    """
    from datetime import datetime, timedelta

    start = datetime.strptime(start_time, "%H:%M:%S")
    times = [start.strftime("%H:%M")]

    for _ in range(1, num_slots):
        start += timedelta(minutes=slot_duration)
        times.append(start.strftime("%H:%M"))

    return times

def get_slots_for_time(slots: List[Dict], start_time: str) -> List[int]:
    """
    Возвращает список slot_ids для указанного времени.
    :param slots: Список временных промежутков из API.
    :param start_time: Время, с которого пользователь хочет начать тренировку (например, '08:00:00').
    :return: Список slot_ids, соответствующих полуторочасовому интервалу.
    """
    for period in slots:
        all_start_times = generate_start_times(
            period["start_time"], len(period["slot_ids"]), slot_duration=30
        )

        # Если start_time есть в данном периоде
        if start_time in all_start_times:
            start_index = all_start_times.index(start_time)
            # Проверяем, есть ли достаточно слотов для полуторочасовой тренировки
            if start_index + 2 < len(period["slot_ids"]):
                return period["slot_ids"][start_index : start_index + 3]  # Возвращаем 3 слота

    return []
