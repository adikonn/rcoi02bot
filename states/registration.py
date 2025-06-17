from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    waiting_for_family = State()
    waiting_for_name = State()
    waiting_for_father = State()
    waiting_for_number = State()
    waiting_for_class = State()
