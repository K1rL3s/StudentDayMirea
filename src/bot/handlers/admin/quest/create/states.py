from aiogram.fsm.state import State, StatesGroup


class CreateQuestStates(StatesGroup):
    order = State()
    title = State()
    description = State()
    task = State()
    image = State()
    reward = State()
    answer = State()
    confirm = State()
