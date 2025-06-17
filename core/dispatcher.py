from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import registration, results, common
from middleware.logging import LoggingMiddleware
from middleware.error_handler import ErrorHandlerMiddleware


def create_dispatcher() -> Dispatcher:
    """Создание и настройка диспетчера"""
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация middleware
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(ErrorHandlerMiddleware())

    # Регистрация роутеров
    dp.include_router(registration.router)
    dp.include_router(results.router)
    dp.include_router(common.router)

    return dp
