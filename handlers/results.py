from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command
from services.result_service import result_service
from utils.phrases import get_phrase
from utils.images import create_table_image
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("get_result"))
async def get_result_command(message: Message) -> None:
    """Обработчик команды /get_result"""
    await message.answer("⏳ Получаю ваши результаты, пожалуйста подождите...")

    try:
        result = await result_service.get_user_result(message.from_user.id)

        if result == "Пользователь не найден. Пожалуйста, пройдите регистрацию командой /start":
            await message.answer(result)
        elif result == "error server":
            await message.answer(
                "❌ Ошибка сервера. Сайт временно недоступен. "
                "Попробуйте позже."
            )
        elif result == "account does not exist. please check and try again":
            await message.answer(
                "❌ Аккаунт не найден. Проверьте правильность введенных "
                "при регистрации данных. При необходимости используйте "
                "команду /reregister для повторной регистрации."
            )
        else:
            headers, data, keyboard = result[0][0], result[0][1], result[1]
            table_image = BufferedInputFile(file=create_table_image(headers, data).getvalue(), filename='image.png')
            await message.answer_photo(photo=table_image, caption=f"📊 **Ваши результаты:**\n\n***«{get_phrase()}»***", parse_mode="Markdown", reply_markup=keyboard)

    except Exception as e:
        logger.error(f"Error in get_result_command: {str(e)}")
        await message.answer(
            "❌ Произошла ошибка при получении результатов. "
            "Попробуйте позже или обратитесь к администратору."
        )
