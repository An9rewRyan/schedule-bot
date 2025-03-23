import httpx
from typing import List, Dict, Any
from datetime import date, datetime, timedelta, time
from w3lib.url import add_or_replace_parameter

API_BASE_URL = "http://0.0.0.0:8000/api"


async def delete_booking(booking_id: int, telegram_id: int):
    url_deleted = False
    async with httpx.AsyncClient() as client:
        url = f"{API_BASE_URL}/bookings"
        payload = {"telegram_id": telegram_id}
        url = add_or_replace_parameter(url, "booking_id", str(booking_id))
        url = add_or_replace_parameter(url, 'telegram_id', telegram_id)
        response = await client.delete(url=url)
        if response.status_code == 200:
            url_deleted = True
    return url_deleted


async def get_bookings_for_day(selected_date: date) -> List[Dict[str, Any]]:
    """
    Получает все записи на конкретный день (для администратора).
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/bookings",
                                    params={"booking_date": selected_date.isoformat()})
        if response.status_code == 200:
            data = response.json()
            return data  # Возвращаем список всех записей
        raise Exception(f"Ошибка получения записей на день: {response.text}")


async def get_bookings_for_user(telegram_id: int) -> List[Dict[str, Any]]:
    """
    Получает все записи на конкретный день (для администратора).
    """
    async with httpx.AsyncClient() as client:
        params = {'telegram_id': telegram_id}
        response = await client.get(f"{API_BASE_URL}/bookings", params=params)
        if response.status_code == 200:
            data = response.json()
            return data  # Возвращаем список всех записей
        raise Exception(f"Ошибка получения записей на день: {response.text}")


async def book_slots(start_time: str, end_time: str, selected_day: str, user_id: int) -> Dict[str, Any]:
    """
    Делает запись на выбранные слоты.
    """
    async with httpx.AsyncClient() as client:
        payload = {"booking": {"date": selected_day, "start_time": start_time, "end_time": end_time},
                   "user": {"telegram_id": user_id}}

        url = f"{API_BASE_URL}/bookings"
        response = await client.post(url, json=payload)

        if response.status_code == 200:
            return response.json()  # Возвращаем результат записи
        elif response.status_code == 404:
            raise Exception(f"Ошибка 404: маршрут не найден. Проверьте URL: {url}")
        else:
            raise Exception(f"Ошибка записи на слоты: {response.text}")
