import asyncio
import logging
import sys
from core.bot import create_bot
from core.dispatcher import create_dispatcher
from database.repository import user_repository
from services.notification_service import NotificationService
from config.settings import settings


async def main() -> None:
    """Основная функция приложения"""
    # Настройка логирования
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting bot...")

    # Инициализация базы данных
    await user_repository.init_db()
    logger.info("Database initialized")

    # Создание бота и диспетчера
    bot = create_bot()
    dp = create_dispatcher()

    # Создание и запуск сервиса уведомлений
    notification_service = NotificationService(bot)
    monitoring_task = asyncio.create_task(notification_service.start_monitoring())

    try:
        logger.info("Bot started successfully")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped with error: {str(e)}")
    finally:
        await notification_service.stop_monitoring()
        monitoring_task.cancel()
        try:
            await monitoring_task
        except asyncio.CancelledError:
            pass
        await bot.session.close()
        logger.info("Bot shutdown completed")


if __name__ == "__main__":
    asyncio.run(main())
