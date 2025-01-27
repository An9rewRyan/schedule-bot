from fastapi import APIRouter

from .endpoints.auth import auth_router
from .endpoints.timeslots import timeslots_router

main_router = APIRouter()

main_router.include_router(
    auth_router,
)

main_router.include_router(
    timeslots_router
)
