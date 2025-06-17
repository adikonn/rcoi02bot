import pytest
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
from handlers.registration import start_command, process_family
from states.registration import RegistrationStates


@pytest.mark.asyncio
async def test_start_command():
    """Тест команды /start"""
    request = MockedBot(MessageHandler(start_command))
    calls = await request.query(message=MESSAGE.as_object(text="/start"))

    answer_message = calls.send_message.fetchone()
    assert "Добро пожаловать" in answer_message.text
    assert calls.fsm.get_state() == RegistrationStates.waiting_for_family


@pytest.mark.asyncio
async def test_process_family_valid():
    """Тест обработки корректной фамилии"""
    request = MockedBot(MessageHandler(process_family))
    request.fsm.set_state(RegistrationStates.waiting_for_family)

    calls = await request.query(message=MESSAGE.as_object(text="Иванов"))

    answer_message = calls.send_message.fetchone()
    assert "Введите ваше имя" in answer_message.text
    assert calls.fsm.get_state() == RegistrationStates.waiting_for_name


@pytest.mark.asyncio
async def test_process_family_invalid():
    """Тест обработки некорректной фамилии"""
    request = MockedBot(MessageHandler(process_family))
    request.fsm.set_state(RegistrationStates.waiting_for_family)

    calls = await request.query(message=MESSAGE.as_object(text="123"))

    answer_message = calls.send_message.fetchone()
    assert "❌" in answer_message.text
    assert calls.fsm.get_state() == RegistrationStates.waiting_for_family
