import os

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DB_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:1234@localhost:5432/main')

engine = create_async_engine(DB_URL, echo=True, future=True)
