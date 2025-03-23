from .api.routers import main_router
from src.utilities.exceptions import *

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.utilities.exceptions import BaseBookingException

app = FastAPI(title="API_NAME",
              description="API_DESC",
              version="0.2.0",
              docs_url='/api/docs',
              redoc_url='/api/redoc',
              openapi_url='/api/openapi.json')


@app.exception_handler(BaseBookingException)
async def booking_exception_handler(request: Request, exc: BaseBookingException):
    if isinstance(exc, TooSmallBookingDurationException):
        return JSONResponse(status_code=400, content={"detail": "Booking duration too small"})
    elif isinstance(exc, NotEnoughSlotsException):
        return JSONResponse(status_code=400, content={"detail": "Free slots amount are less than requested"})
    elif isinstance(exc, RequestedSlotsBusyException):
        return JSONResponse(status_code=400, content={"detail": "Some of requested slots are already occupied"})
    elif isinstance(exc, BookingSaveFailedException):
        return JSONResponse(status_code=500, content={"detail": "Failed to save booking slot"})
    elif isinstance(exc, BookingNotFoundException):
        return JSONResponse(status_code=404, content={"detail": "Failed to find booking"})


@app.exception_handler(BaseUserException)
async def booking_exception_handler(request: Request, exc: BaseBookingException):
    if isinstance(exc, UserNotFoundException):
        return JSONResponse(status_code=404, content={"detail": "Failed to find requested user"})
    elif isinstance(exc, UserUnauthorizedException):
        return JSONResponse(status_code=401, content={"detail": "Anauthorized"})


app.include_router(
    main_router,
    prefix="/api",
    tags=["users"],
)
