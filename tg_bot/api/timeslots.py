import httpx
from typing import List, Dict, Any
from datetime import date, datetime, timedelta

API_BASE_URL = "http://0.0.0.0:8000/api"  # Замените на ваш реальный URL API


async def get_free_days(current_date: date = date.today(), telegram_id: int = None) -> List[str]:
    """
    Получает все свободные дни на текущей неделе.
    """
    start_of_week = current_date  # Понедельник текущей недели
    end_of_week = start_of_week + timedelta(days=6)  # Воскресенье текущей недели

    free_days = []
    for single_date in (start_of_week + timedelta(days=n) for n in range(7)):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/slots/available",
                                        params={"selected_date": single_date.isoformat(), "telegram_id": telegram_id})
            if response.status_code == 200:
                data = response.json()
                if data["available_periods"]:  # Если есть свободные слоты в этот день
                    free_days.append(single_date.isoformat())

    return free_days


async def get_available_slots(selected_date: str, telegram_id: int) -> List[Dict[str, Any]]:
    """
    Получает все доступные временные промежутки на выбранный день.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/slots/available",
                                    params={"selected_date": selected_date, "telegram_id": telegram_id})
        if response.status_code == 200:
            data = response.json()
            return data.get("available_periods", [])  # Список доступных временных промежутков
        raise Exception(f"Ошибка получения доступных слотов: {response.text}")


async def get_bookings_for_day(selected_date: date) -> List[Dict[str, Any]]:
    """
    Получает все записи на конкретный день (для администратора).
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/slots/bookings",
                                    params={"selected_date": selected_date.isoformat()})
        if response.status_code == 200:
            data = response.json()
            return data  # Возвращаем список всех записей
        raise Exception(f"Ошибка получения записей на день: {response.text}")


async def book_slots(selected_slots: List[int], user_id: int) -> Dict[str, Any]:
    """
    Делает запись на выбранные слоты.
    """
    async with httpx.AsyncClient() as client:
        payload = selected_slots  # Список слотов в теле запроса
        params = {"telegram_id": user_id}  # user_id передаём как query-параметр

        url = f"{API_BASE_URL}/slots/booking"
        print(f"POST {url} | params={params} | json={payload}")  # Логируем запрос для отладки

        response = await client.post(url, json=payload, params=params)

        if response.status_code == 200:
            return response.json()  # Возвращаем результат записи
        elif response.status_code == 404:
            raise Exception(f"Ошибка 404: маршрут не найден. Проверьте URL: {url}")
        else:
            raise Exception(f"Ошибка записи на слоты: {response.text}")
