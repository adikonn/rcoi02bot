from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from typing import Callable, Dict, Any, Awaitable
import logging
import time

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        start_time = time.time()

        if isinstance(event, Update):
            user_id = None
            if event.message:
                user_id = event.message.from_user.id
                logger.info(f"Message from user {user_id}: {event.message.text}")
            elif event.callback_query:
                user_id = event.callback_query.from_user.id
                logger.info(f"Callback query from user {user_id}: {event.callback_query.data}")

        try:
            result = await handler(event, data)
            execution_time = time.time() - start_time
            logger.info(f"Handler executed in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Handler failed after {execution_time:.3f}s: {str(e)}")
            raise
