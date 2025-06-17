import pytest
from unittest.mock import AsyncMock, patch
from services.result_service import ResultService
from database.models import User


@pytest.mark.asyncio
async def test_get_user_result_user_not_found():
    """Тест получения результата для несуществующего пользователя"""
    service = ResultService()

    with patch('services.result_service.user_repository') as mock_repo:
        mock_repo.get_user_by_id.return_value = None

        result = await service.get_user_result(123)
        assert "не найден" in result


@pytest.mark.asyncio
async def test_get_user_result_success():
    """Тест успешного получения результата"""
    service = ResultService()
    mock_user = User(
        user_id=123,
        family="Иванов",
        name="Иван",
        father="Иванович",
        number="123456",
        class_="11"
    )

    with patch('services.result_service.user_repository') as mock_repo, \
            patch('services.result_service.get_content') as mock_get_content, \
            patch('services.result_service.print_result') as mock_print_result:
        mock_repo.get_user_by_id.return_value = mock_user
        mock_get_content.return_value = {'success': True, 'response': 'html'}
        mock_print_result.return_value = "Результаты"

        result = await service.get_user_result(123)
        assert result == "Результаты"
