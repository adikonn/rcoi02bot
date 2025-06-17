from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database.repository import user_repository
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    """Обработчик команды /help"""
    help_text = """
📋 **Доступные команды:**

/start - Начать работу и пройти регистрацию
/help - Показать эту справку
/profile - Посмотреть данные профиля
/reregister - Пройти регистрацию заново
/get_result - Получить текущие результаты

🔔 **Автоматические уведомления:**
Бот автоматически проверяет изменения в ваших результатах каждые 10 минут и уведомляет о них.

❓ **Нужна помощь?**
Обратитесь к администратору бота.
    """
    await message.answer(help_text, parse_mode="Markdown")


@router.message(Command("profile"))
async def profile_command(message: Message) -> None:
    """Обработчик команды /profile"""
    user = await user_repository.get_user_by_id(message.from_user.id)

    if not user:
        await message.answer(
            "Вы не зарегистрированы. Используйте команду /start для регистрации."
        )
        return

    profile_text = f"""
👤 **Ваш профиль:**

**Фамилия:** {user.family}
**Имя:** {user.name}
**Отчество:** {user.father}
**Серия документа:** {user.number}
**Класс:** {user.class_}

Для изменения данных используйте команду /reregister
    """
    await message.answer(profile_text, parse_mode="Markdown")
