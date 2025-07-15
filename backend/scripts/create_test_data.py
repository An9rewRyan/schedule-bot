#!/usr/bin/env python3
"""
Скрипт для создания тестовых данных в базе данных
"""

import sys
import os
import asyncio
from datetime import date, time, timedelta
from pathlib import Path

# Добавляем путь к src в sys.path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from src.repository.db import engine
from src.models.db import TimeSlot, User
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

# Создаем асинхронную сессию
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_test_timeslots():
    """Создает тестовые таймслоты на ближайшие 7 дней"""
    print("🎯 Создание тестовых таймслотов...")
    
    # Временные слоты для тренировок
    time_slots = [
        (time(9, 0), time(10, 0)),   # 9:00 - 10:00
        (time(10, 0), time(11, 0)),  # 10:00 - 11:00
        (time(11, 0), time(12, 0)),  # 11:00 - 12:00
        (time(14, 0), time(15, 0)),  # 14:00 - 15:00
        (time(15, 0), time(16, 0)),  # 15:00 - 16:00
        (time(16, 0), time(17, 0)),  # 16:00 - 17:00
        (time(17, 0), time(18, 0)),  # 17:00 - 18:00
        (time(18, 0), time(19, 0)),  # 18:00 - 19:00
        (time(19, 0), time(20, 0)),  # 19:00 - 20:00
    ]
    
    # Названия дней недели
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    
    # Создаем таймслоты на ближайшие 7 дней
    today = date.today()
    created_count = 0
    
    async with async_session() as session:
        # Проверяем, есть ли уже таймслоты
        result = await session.exec(select(TimeSlot))
        existing_slots = result.all()
        
        if existing_slots:
            print(f"⚠️  Найдено {len(existing_slots)} существующих таймслотов")
            response = input("Создать дополнительные таймслоты? (y/n): ")
            if response.lower() != 'y':
                print("❌ Создание отменено")
                return
        
        for day_offset in range(7):  # Следующие 7 дней
            current_date = today + timedelta(days=day_offset)
            weekday_name = weekdays[current_date.weekday()]
            
            # Пропускаем воскресенье (день отдыха)
            if current_date.weekday() == 6:  # 6 = воскресенье
                continue
                
            for start_time, end_time in time_slots:
                # Создаем таймслот
                timeslot = TimeSlot(
                    date=current_date,
                    start_time=start_time,
                    end_time=end_time,
                    weekday=weekday_name
                )
                
                session.add(timeslot)
                created_count += 1
        
        # Сохраняем изменения
        await session.commit()
        print(f"✅ Создано {created_count} таймслотов")

async def create_test_users():
    """Создает тестовых пользователей"""
    print("👥 Создание тестовых пользователей...")
    
    test_users = [
        {
            "telegram_id": 123456789,
            "first_name": "Тестовый",
            "second_name": "Пользователь",
            "age": 25,
            "phone_number": "+79001234567",
            "is_admin": False
        },
        {
            "telegram_id": 987654321,
            "first_name": "Админ",
            "second_name": "Тестовый",
            "age": 30,
            "phone_number": "+79009876543",
            "is_admin": True
        }
    ]
    
    async with async_session() as session:
        created_count = 0
        
        for user_data in test_users:
            # Проверяем, существует ли пользователь
            result = await session.exec(
                select(User).where(User.telegram_id == user_data["telegram_id"])
            )
            existing_user = result.first()
            
            if not existing_user:
                user = User(**user_data)
                session.add(user)
                created_count += 1
            else:
                print(f"⚠️  Пользователь с telegram_id {user_data['telegram_id']} уже существует")
        
        await session.commit()
        print(f"✅ Создано {created_count} пользователей")

async def show_existing_data():
    """Показывает существующие данные в базе"""
    print("📊 Существующие данные в базе:")
    
    async with async_session() as session:
        # Показываем таймслоты
        result = await session.exec(select(TimeSlot))
        timeslots = result.all()
        print(f"🎯 Таймслоты: {len(timeslots)}")
        
        if timeslots:
            print("Последние 5 таймслотов:")
            for slot in timeslots[-5:]:
                print(f"  - {slot.date} {slot.start_time}-{slot.end_time}")
        
        # Показываем пользователей
        result = await session.exec(select(User))
        users = result.all()
        print(f"👥 Пользователи: {len(users)}")
        
        if users:
            print("Пользователи:")
            for user in users:
                print(f"  - {user.first_name} {user.second_name} (ID: {user.telegram_id})")

async def main():
    print("=" * 60)
    print("🎯 Создание тестовых данных для Telegram Mini App")
    print("=" * 60)
    
    try:
        # Показываем существующие данные
        await show_existing_data()
        print()
        
        # Создаем тестовые данные
        await create_test_timeslots()
        print()
        await create_test_users()
        print()
        
        # Показываем результат
        print("📊 Итоговые данные:")
        await show_existing_data()
        
        print("\n✅ Тестовые данные созданы успешно!")
        print("🚀 Теперь можно запускать Mini App")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Проверьте настройки базы данных в backend/src/repository/db.py")

if __name__ == "__main__":
    asyncio.run(main()) 