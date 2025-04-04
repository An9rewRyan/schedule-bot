import httpx
import logging

API_BASE_URL = "http://0.0.0.0:8000/api"


async def get_user(telegram_id: int):
    user_name = ""
    is_admin = False
    is_authenticated = False
    async with httpx.AsyncClient() as client:
        payload = {'telegram_id': telegram_id}
        response = await client.request(url=f"{API_BASE_URL}/authenticate", method='POST', json=payload)
        if response.status_code == 200:
            jo = response.json()
            is_authenticated = True
            is_admin = jo['is_admin']
            user_name = jo['user_name']
        return is_authenticated, is_admin, user_name


async def register_user(user_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.request(url=f"{API_BASE_URL}/register", method='POST', json=user_data)
    return response


async def set_admin_role(telegram_id: int) -> httpx.Response:
    """
    Отправляет PATCH-запрос на API для назначения роли администратора пользователю с данным telegram_id.
    """
    async with httpx.AsyncClient() as client:
        response = await client.patch(url=f"{API_BASE_URL}/users/{telegram_id}/admin")
        return response
