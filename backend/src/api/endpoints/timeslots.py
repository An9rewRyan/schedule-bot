import logging
from datetime import datetime, date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from src.api.dependencies import get_repository
from src.repository.crud import TimeslotCRUDRepository, UserCRUDRepository
from src.models.schemas import TimeSlotInfoVisitors
from src.models.db import TimeSlot

timeslots_router = APIRouter()

# Настройка логгера
logger = logging.getLogger(__name__)

@timeslots_router.options("/available-days")
async def options_available_days(response: Response):
    """Handle CORS preflight requests for available-days endpoint"""
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"message": "OK"}

@timeslots_router.options("/")
async def options_timeslots(response: Response, selected_date: Optional[date] = None, telegram_id: Optional[int] = None):
    """Handle CORS preflight requests for timeslots endpoint"""
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"message": "OK"}

@timeslots_router.get("/available-days")
async def get_available_days(
    timeslot_repo: TimeslotCRUDRepository = Depends(get_repository(repo_type=TimeslotCRUDRepository))
):
    """
    Получить доступные дни для бронирования
    """
    try:
        logger.info("=== ЗАПРОС НА ПОЛУЧЕНИЕ ДОСТУПНЫХ ДНЕЙ ===")
        logger.info(f"Время запроса: {datetime.now()}")
        
        # Получаем доступные дни
        logger.info("Получение доступных дней из репозитория...")
        
        # Получаем таймслоты на ближайшие 7 дней
        from datetime import timedelta
        today = date.today()
        available_days = []
        
        for i in range(7):
            check_date = today + timedelta(days=i)
            logger.info(f"Проверяем дату: {check_date}")
            # Получаем все слоты для этой даты
            slots = await timeslot_repo.get_timeslots_by_date(check_date)
            logger.info(f"Найдено слотов для {check_date}: {len(slots) if slots else 0}")
            if slots:
                available_days.append(check_date.isoformat())
        
        logger.info(f"Найдено доступных дней: {len(available_days)}")
        logger.info(f"Доступные дни: {available_days}")
        
        result = {"available_days": available_days}
        logger.info(f"Возвращаем результат: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"ОШИБКА при получении доступных дней: {str(e)}")
        logger.error(f"Тип ошибки: {type(e)}")
        import traceback
        logger.error(f"Трассировка: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении доступных дней: {str(e)}")


@timeslots_router.get("/")
async def get_timeslots(
    selected_date: date = Query(..., description="Выбранная дата"),
    telegram_id: Optional[int] = Query(None, description="ID пользователя Telegram"),
    timeslot_repo: TimeslotCRUDRepository = Depends(get_repository(repo_type=TimeslotCRUDRepository)),
    user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository)),
):
    """
    Получить тайм-слоты для выбранной даты
    """
    try:
        logger.info("=== ЗАПРОС НА ПОЛУЧЕНИЕ ТАЙМ-СЛОТОВ ===")
        logger.info(f"Время запроса: {datetime.now()}")
        logger.info(f"Выбранная дата: {selected_date}")
        logger.info(f"Telegram ID: {telegram_id}")
        
        # Проверяем пользователя, если передан telegram_id
        user = None
        if telegram_id:
            logger.info(f"Поиск пользователя с telegram_id: {telegram_id}")
            try:
                user = await user_repo.get_user_by_telegram_id(telegram_id)
                if user:
                    logger.info(f"Найден пользователь: {user.first_name} {user.second_name}")
                else:
                    logger.warning(f"Пользователь с telegram_id {telegram_id} не найден")
            except Exception as user_error:
                logger.error(f"Ошибка при поиске пользователя: {user_error}")
        
        # Получаем тайм-слоты
        logger.info("Получение тайм-слотов из репозитория...")
        from src.services import TimeslotService
        
        timeslot_service = TimeslotService(user_repo=user_repo, timeslot_repo=timeslot_repo)
        free_slots = await timeslot_service.get_free_slots(telegram_id=telegram_id, selected_date=selected_date)
        
        logger.info(f"Найдено свободных слотов: {len(free_slots)}")
        for slot in free_slots:
            logger.info(f"Слот ID {slot.id}: {slot.start_time}-{slot.end_time}")
        
        result = {"available_periods": [TimeSlotInfoVisitors.from_orm(slot) for slot in free_slots]}
        logger.info(f"Возвращаем результат с {len(result['available_periods'])} слотами")
        
        return result
        
    except Exception as e:
        logger.error(f"ОШИБКА при получении тайм-слотов: {str(e)}")
        logger.error(f"Тип ошибки: {type(e)}")
        import traceback
        logger.error(f"Трассировка: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении тайм-слотов: {str(e)}")
