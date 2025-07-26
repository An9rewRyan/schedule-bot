import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.routers import main_router
from src.utilities.exceptions import UserNotFoundException, BookingNotFoundException, BookingRequestException

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Приложение запущено")
    yield

app = FastAPI(
    title="Schedule Bot API",
    description="API для бота планирования встреч",
    version="1.0.0",
    lifespan=lifespan
)

# CORS настройки
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://cf617961ccde.ngrok-free.app"
]

logger.info(f"Настроенные CORS origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для логирования всех запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Логируем входящий запрос
    logger.info("="*50)
    logger.info(f"ВХОДЯЩИЙ ЗАПРОС: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Query params: {dict(request.query_params)}")
    logger.info(f"Client: {request.client}")
    
    # Логируем User-Agent для определения источника
    user_agent = request.headers.get("user-agent", "")
    if "TelegramBot" in user_agent or "Telegram" in user_agent:
        logger.info("🤖 ЗАПРОС ОТ TELEGRAM")
    else:
        logger.info("🌐 ЗАПРОС ОТ БРАУЗЕРА")
    
    # Обрабатываем запрос
    response = await call_next(request)
    
    # Логируем ответ
    process_time = time.time() - start_time
    logger.info(f"ОТВЕТ: {response.status_code}")
    logger.info(f"Время обработки: {process_time:.4f}s")
    logger.info("="*50)
    
    return response

# Обработчики исключений
@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    logger.error(f"UserNotFoundException: {exc}")
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )

@app.exception_handler(BookingNotFoundException)
async def booking_not_found_exception_handler(request: Request, exc: BookingNotFoundException):
    logger.error(f"BookingNotFoundException: {exc}")
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )

@app.exception_handler(BookingRequestException)
async def booking_request_exception_handler(request: Request, exc: BookingRequestException):
    logger.error(f"BookingRequestException: {exc}")
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": exc.errors()}
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

# Добавляем обработку OPTIONS запросов для CORS
@app.options("/{full_path:path}")
async def options_handler(request: Request):
    """Обработка OPTIONS запросов для CORS"""
    response = Response()
    origin = request.headers.get("origin")
    
    if origin in origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
    
    return response

# Подключение роутеров
app.include_router(main_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Schedule Bot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Запуск сервера на порту {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
