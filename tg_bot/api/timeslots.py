import httpx
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta

API_BASE_URL = "https://7db1d64ccc1e.ngrok-free.app/api"  # Замените на ваш реальный URL API


async def get_free_days(current_date: date = date.today(), telegram_id: Optional[int] = None) -> List[str]:
    """
    Получает все свободные дни для бронирования.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/slots/available-days")
        if response.status_code == 200:
            data = response.json()
            return data.get("available_days", [])
        else:
            raise Exception(f"Ошибка получения доступных дней: {response.text}")


async def get_available_slots(selected_date: str, telegram_id: int) -> List[Dict[str, Any]]:
    """
    Получает все доступные временные промежутки на выбранный день.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/slots",
                                    params={"selected_date": selected_date, "telegram_id": telegram_id})
        if response.status_code == 200:
            data = response.json()
            return data.get("available_periods", []) # Список доступных временных промежутков
        raise Exception(f"Ошибка получения доступных слотов: {response.text}")