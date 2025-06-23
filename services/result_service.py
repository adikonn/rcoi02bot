from typing import Optional

from sqlalchemy.util import await_only
import asyncio
from database.repository import user_repository
from utils.parsers import get_content, extract_more_tables, print_result, extract_table_tb_result, get_page, get_images, extract_page_info, create_inline_keyboard
from utils.images import create_table_image_blanks
import logging

logger = logging.getLogger(__name__)


class ResultService:
    async def get_user_result(self, user_id: int):
        """Получение результатов пользователя"""
        user = await user_repository.get_user_by_id(user_id)
        if not user:
            return "Пользователь не найден. Пожалуйста, пройдите регистрацию командой /start"

        try:
            content = get_content(
                family=user.family,
                name=user.name,
                father=user.father,
                number=user.number,
                class_=user.class_
            )
            result = print_result(content)
            if 'error' in result or 'account' in result:
                return result
            keyboard = create_inline_keyboard(extract_page_info(content))
            return result, keyboard
        except Exception as e:
            logger.error(f"Error getting result for user {user_id}: {str(e)}")
            return "Произошла ошибка при получении результатов. Попробуйте позже."

    async def check_result_changes(self, user_id: int, count: int = 0) -> Optional[tuple]:
        """Проверка изменений в результатах пользователя"""
        user = await user_repository.get_user_by_id(user_id)
        if not user:
            return None

        try:
            content = get_content(
                family=user.family,
                name=user.name,
                father=user.father,
                number=user.number,
                class_=user.class_
            )

            current_result = extract_table_tb_result(content)
            if current_result == 'error server':
                if count < 6:
                    await asyncio.sleep(100)  # Короткая пауза при ошибке
                    return await self.check_result_changes(user_id, count+1)
                else:
                    return None
            if current_result == 'account does not exist. please check and try again':
                return None
            if current_result != user.last_result:
                prev = user.last_result
                await user_repository.update_user_result(user_id, current_result)
                return current_result, prev

            return None
        except Exception as e:
            logger.error(f"Error checking result changes for user {user_id}: {str(e)}")
            return None
    async def get_images(self, user_id: int, page_id: str, count=0):
        user = await user_repository.get_user_by_id(user_id)
        if not user:
            return None, None

        try:
            content = get_page(
                family=user.family,
                name=user.name,
                father=user.father,
                number=user.number,
                class_=user.class_,
                page_id=page_id
            )
            if not content['success']:
                return None, None
            try:
                images = get_images(html_content=content)
                tables = extract_more_tables(html_content=content)
                image_tables = []
                if tables:
                    image_tables = [create_table_image_blanks(*table) for table in tables]
                return images, image_tables
            except Exception as e:
                logger.error(f"Error download photos for user {user_id}: {str(e)}")
                return None, None
        except Exception as e:
            logger.error(f"Error download photos for user {user_id}: {str(e)}")
            return None, None

result_service = ResultService()
