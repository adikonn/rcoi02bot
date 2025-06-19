from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states.registration import RegistrationStates
from database.repository import user_repository
from utils.phrases import get_phrase
from utils.images import create_table_image
import re
import logging
from utils.parsers import get_content, print_result, extract_table_tb_result
logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext) -> None:
    """Обработчик команды /start"""
    msg = await message.answer(
        "👋 Добро пожаловать в бот для проверки результатов ГИА!\n\n"
        "Для начала работы необходимо пройти регистрацию.\n"
        "Введите вашу фамилию:"
    )
    await state.set_state(RegistrationStates.waiting_for_family)
    await state.update_data(message=msg)

@router.message(Command("reregister"))
async def reregister_command(message: Message, state: FSMContext) -> None:
    """Обработчик команды /reregister"""
    msg = await message.answer("Начинаем регистрацию заново.\nВведите вашу фамилию:")

    await state.set_state(RegistrationStates.waiting_for_family)
    await state.update_data(message=msg)



@router.message(StateFilter(RegistrationStates.waiting_for_family))
async def process_family(message: Message, state: FSMContext) -> None:
    """Обработка ввода фамилии"""
    await message.delete()
    family = message.text.strip()
    data = await state.get_data()
    msg = data['message']
    if not family or not family.replace('-', '').replace(' ', '').isalpha():
        await msg.edit_text(
            "❌ Фамилия должна содержать только буквы, пробелы и дефисы.\n"
            "Попробуйте еще раз:"
        )
        return

    await state.update_data(family=family)
    await msg.edit_text("Введите ваше имя:")
    await state.set_state(RegistrationStates.waiting_for_name)


@router.message(StateFilter(RegistrationStates.waiting_for_name))
async def process_name(message: Message, state: FSMContext) -> None:
    await message.delete()

    """Обработка ввода имени"""
    data = await state.get_data()
    msg = data['message']

    name = message.text.strip()

    if not name or not name.replace('-', '').replace(' ', '').isalpha():
        await msg.edit_text(
            "❌ Имя должно содержать только буквы, пробелы и дефисы.\n"
            "Попробуйте еще раз:"
        )
        return

    await state.update_data(name=name)
    await msg.edit_text("Введите ваше отчество:")
    await state.set_state(RegistrationStates.waiting_for_father)


@router.message(StateFilter(RegistrationStates.waiting_for_father))
async def process_father(message: Message, state: FSMContext) -> None:
    await message.delete()

    """Обработка ввода отчества"""
    data = await state.get_data()
    msg = data['message']

    father = message.text.strip()

    if not father or not father.replace('-', '').replace(' ', '').isalpha():
        await msg.edit_text(
            "❌ Отчество должно содержать только буквы, пробелы и дефисы.\n"
            "Попробуйте еще раз:"
        )
        return

    await state.update_data(father=father)
    await msg.edit_text("Введите серию документа (6-значный номер):")
    await state.set_state(RegistrationStates.waiting_for_number)


@router.message(StateFilter(RegistrationStates.waiting_for_number))
async def process_number(message: Message, state: FSMContext) -> None:
    await message.delete()

    """Обработка ввода серии документа"""
    data = await state.get_data()
    msg = data['message']

    number = message.text.strip()

    if not re.match(r'^\d{6}$', number):
        await msg.edit_text(
            "❌ Серия документа должна состоять из 6 цифр.\n"
            "Попробуйте еще раз:"
        )
        return

    await state.update_data(number=number)
    await msg.edit_text("Введите ваш класс (9 или 11):")
    await state.set_state(RegistrationStates.waiting_for_class)


@router.message(StateFilter(RegistrationStates.waiting_for_class))
async def process_class(message: Message, state: FSMContext) -> None:
    await message.delete()

    """Обработка ввода класса"""
    data = await state.get_data()
    msg = data['message']
    class_value = message.text.strip()

    if class_value not in ['9', '11']:
        await msg.edit_text(
            "❌ Класс должен быть 9 или 11.\n"
            "Попробуйте еще раз:"
        )
        return

    # Получаем все данные из состояния
    data = await state.get_data()
    data['class_'] = class_value

    try:
        content = get_content(family=data['family'],
            name=data['name'],
            father=data['father'],
            number=data['number'],
            class_=data['class_'])
        result = print_result(content)
        if result == "error server":
            await msg.edit_text(
                "❌ Ошибка сервера. "
                "Попробуйте позже."
            )
        elif result == "account does not exist. please check and try again":
            await msg.edit_text(
                "❌ Аккаунт не найден. Проверьте правильность введенных "
                "при регистрации данных."
            )
        else:
            await msg.delete()
            table_image = BufferedInputFile(file=create_table_image(*result).getvalue(), filename='image.png')
            # Сохраняем пользователя в базу данных
            await user_repository.create_user(
                user_id=message.from_user.id,
                family=data['family'],
                name=data['name'],
                father=data['father'],
                number=data['number'],
                class_=data['class_']
            )
            current_result = extract_table_tb_result(content)
            await user_repository.update_user_result(message.chat.id, current_result)
            await message.answer_photo(photo=table_image, caption=f"📊 **Ваши результаты:**\n\n{result}\n***«{get_phrase()}»***", parse_mode='Markdown')
            await message.answer(
                "✅ Регистрация успешно завершена!\n\n"
                "Теперь вы можете:\n"
                "• Использовать /get_result для получения результатов\n"
                "• Получать автоматические уведомления об изменениях\n"
                "• Просматривать профиль командой /profile\n\n"
                "Бот будет автоматически проверять изменения каждые 10 минут и оповещать вас, если придут результаты новых экзаменов."
            )

            logger.info(f"User {message.from_user.id} registered successfully")

    except Exception as e:
        logger.error(f"Error saving user {message.from_user.id}: {str(e)}")
        await msg.edit_text(
            "❌ Произошла ошибка при сохранении данных. "
            "Попробуйте зарегистрироваться заново командой /start"
        )

    finally:
        await state.clear()


@router.message(StateFilter(RegistrationStates))
async def process_invalid_input(message: Message, state: FSMContext) -> None:
    await message.delete()

    """Обработка некорректного ввода во время регистрации"""
    data = await state.get_data()
    msg = data['message']

    current_state = await state.get_state()

    if current_state == RegistrationStates.waiting_for_family:
        text = "Пожалуйста, введите вашу фамилию:"
    elif current_state == RegistrationStates.waiting_for_name:
        text = "Пожалуйста, введите ваше имя:"
    elif current_state == RegistrationStates.waiting_for_father:
        text = "Пожалуйста, введите ваше отчество:"
    elif current_state == RegistrationStates.waiting_for_number:
        text = "Пожалуйста, введите серию документа (6-значный номер):"
    elif current_state == RegistrationStates.waiting_for_class:
        text = "Пожалуйста, введите ваш класс (9 или 11):"
    else:
        text = "Пожалуйста, следуйте инструкциям регистрации."

    await msg.edit_text(text)
