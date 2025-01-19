from aiogram.fsm.state import State, StatesGroup


class CreateTaskStates(StatesGroup):
    title = State()
    description = State()
    reward = State()
    answer = State()
    confirm = State()
