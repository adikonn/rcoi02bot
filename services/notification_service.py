from aiogram import Bot
from database.repository import user_repository
from services.result_service import result_service
import asyncio
import logging
from config.settings import settings
from utils.phrases import get_phrase
logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.is_running = False

    async def start_monitoring(self) -> None:
        """Запуск мониторинга изменений"""
        if self.is_running:
            return

        self.is_running = True
        logger.info("Starting result monitoring")

        while self.is_running:
            try:
                await self._check_all_users()
                await asyncio.sleep(settings.check_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(60)  # Короткая пауза при ошибке

    async def stop_monitoring(self) -> None:
        """Остановка мониторинга"""
        self.is_running = False
        logger.info("Stopping result monitoring")

    async def _check_all_users(self) -> None:
        """Проверка результатов всех пользователей"""
        users = await user_repository.get_all_users()
        logger.info(f"Checking results for {len(users)} users")

        tasks = []
        for user in users:
            task = asyncio.create_task(self._check_user_result(user.user_id))
            tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _check_user_result(self, user_id: int) -> None:
        """Проверка результата конкретного пользователя"""
        try:
            new_result = await result_service.check_result_changes(user_id)
            if new_result:
                await self._send_notification(user_id, new_result)
        except Exception as e:
            logger.error(f"Error checking user {user_id}: {str(e)}")

    async def _send_notification(self, user_id: int, result: tuple) -> None:
        """Отправка уведомления пользователю"""
        try:
            new, prev = result
            message = f"🔔 Обнаружены изменения в ваших результатах:\n\n{new}\n\n***«{get_phrase()}»***"
            await self.bot.send_message(user_id, message, parse_mode='Markdown')
            logger.info(f"Notification sent to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to send notification to user {user_id}: {str(e)}")
