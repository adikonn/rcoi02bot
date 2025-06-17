from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, ErrorEvent
from typing import Callable, Dict, Any, Awaitable
import logging

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f"Unhandled error: {str(e)}", exc_info=True)

            # Если это обновление с сообщением, отправляем пользователю уведомление об ошибке
            if hasattr(event, 'message') and event.message:
                try:
                    await event.message.answer(
                        "Произошла ошибка при обработке вашего запроса. "
                        "Пожалуйста, попробуйте позже или обратитесь к администратору."
                    )
                except Exception:
                    pass

            raise
