from fastapi import APIRouter
import logging

from backend.src.api.endpoints.users import users_router
from backend.src.api.endpoints.timeslots import timeslots_router
from backend.src.api.endpoints.bookings import bookings_router

logger = logging.getLogger(__name__)

main_router = APIRouter()

print("🔍 DEBUG: Registering users router...")
logger.info("Registering users router...")
main_router.include_router(
    users_router,
    prefix="/users",
    tags=["users"]
)

print("🔍 DEBUG: Registering timeslots router...")
logger.info("Registering timeslots router...")
main_router.include_router(
    timeslots_router,
    prefix="/slots",
    tags=["timeslots"]
)

print("🔍 DEBUG: Registering bookings router...")
logger.info("Registering bookings router...")
main_router.include_router(
    bookings_router,
    prefix="/bookings",
    tags=["bookings"]
)

print("🔍 DEBUG: All routers registered successfully")
logger.info("All routers registered successfully")
