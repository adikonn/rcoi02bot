from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile, CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder
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
@router.callback_query(F.data.startswith("id"))
async def get_more(call: CallbackQuery):
    msg = await call.message.reply("⏳ Получаю ваши бланки, пожалуйста подождите...")
    page_id = call.data.replace("id", "")
    images, table_images = await result_service.get_images(call.message.chat.id, page_id)
    media_list = []
    if table_images:
        for img in table_images:
            media_list.append(BufferedInputFile(file=img.getvalue(), filename='image.png'))
    if images:
        for i in range(len(images)):
            media_list.append(images[i])
    if media_list:
        if len(media_list) > 10:
            media_group1 = MediaGroupBuilder()
            media_group2 = MediaGroupBuilder()
            for i in range(len(media_list)):
                if i < 10:
                        media_group1.add(type='photo', media=media_list[i])
                else:
                    if i == 10:
                        media_group2.add(type='photo', media=media_list[i], caption=f"***{get_phrase()}***", parse_mode="Markdown")
                    else:
                        media_group2.add(type='photo', media=media_list[i])

            await msg.delete()
            await call.message.answer_media_group(media=media_group1.build())
            await call.message.answer_media_group(media=media_group2.build())
        else:
            media_group = MediaGroupBuilder()
            for i in range(len(media_list)):
                if i == 1:
                    media_group.add(type='photo', media=media_list[i], caption=f"***{get_phrase()}***",
                                     parse_mode="Markdown")
                else:
                    media_group.add(type='photo', media=media_list[i])
            await call.message.answer_media_group(media=media_group.build())
    else:
        await msg.edit_text("❌ Произошла ошибка. Попробуйте позже")
