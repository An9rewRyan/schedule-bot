from fastapi import APIRouter

from .endpoints.users import users_router
from .endpoints.timeslots import timeslots_router
from .endpoints.bookings import bookings_router

main_router = APIRouter()

main_router.include_router(
    users_router,
)

main_router.include_router(
    timeslots_router
)

main_router.include_router(
    bookings_router
)
