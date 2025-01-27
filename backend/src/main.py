from fastapi import Depends, FastAPI

from fastapi_limiter.depends import RateLimiter
from .api.routers import main_router
from fastapi import Depends, FastAPI
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from .api.routers import main_router
from src.models.db import User  # Модель таблицы `users`
from src.repository.db import engine

app = FastAPI(title="API_NAME",
              description="API_DESC",
              version="0.2.0",
              docs_url='/api/docs',
              redoc_url='/api/redoc',
              openapi_url='/api/openapi.json')


@app.get("/api/test", dependencies=[Depends(RateLimiter(times=1, seconds=5))])
async def test():
    return {'u didnt': 'break rate limit'}


app.include_router(
    main_router,
    prefix="/api",
    tags=["users"],
)
