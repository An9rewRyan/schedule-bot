import asyncio
from backend.src.repository.db import async_session
from sqlalchemy import text

async def clear_timeslots():
    print('Очистка всех бронирований и связей с таймслотами...')
    async with async_session() as session:
        await session.execute(text('DELETE FROM bookingtimeslotlink'))
        await session.execute(text('DELETE FROM usertimeslotlink'))
        await session.execute(text('DELETE FROM booking'))
        await session.commit()
    print('Очистка завершена.')

if __name__ == '__main__':
    asyncio.run(clear_timeslots()) 