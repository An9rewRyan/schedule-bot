from src.repository.db import engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

import asyncio
from src.models.db import TimeSlot

from datetime import datetime, timedelta, time
from sqlmodel import select


async def get_async_session() -> AsyncSession:
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    session = async_session()  # Создаём сессию
    return session


async def fill_schedule(start_date: datetime, duration: int = 30):
    session = await get_async_session()
    slots = []
    current_date = start_date.date()

    for _ in range(7):  # 7 дней в неделю
        for hour in range(8, 18):  # Рабочие часы с 8:00 до 18:00
            for minute in (0, 30):  # Два слота по 30 минут в каждом часе
                # Стартовое время слота
                slot_start = time(hour=hour, minute=minute, second=0)
                slot_end = (datetime.combine(current_date, slot_start) + timedelta(minutes=duration)).time()

                # Проверяем, существует ли уже такой слот в базе
                statement = select(TimeSlot).where(
                    TimeSlot.date == current_date,
                    TimeSlot.start_time == slot_start,
                    TimeSlot.end_time == slot_end
                )
                existing_slot = await session.execute(statement)

                if existing_slot.first() is None:
                    slots.append(TimeSlot(
                        date=current_date,
                        start_time=slot_start,
                        end_time=slot_end,
                    ))

        # Переход на следующий день
        current_date += timedelta(days=1)

    if slots:
        session.add_all(slots)
        await session.commit()
        print(f"Добавлено {len(slots)} таймслотов.")
    else:
        print("Новых таймслотов не добавлено.")

    await session.close()


# Пример вызова функции
async def main():
    await fill_schedule(datetime.now())


# Запуск
if __name__ == "__main__":
    asyncio.run(main())
