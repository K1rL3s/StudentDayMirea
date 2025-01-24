from aiogram.fsm.state import State, StatesGroup


class CreateQuestStates(StatesGroup):
    order = State()
    title = State()
    description = State()
    task = State()
    image = State()
    reward = State()
    answer = State()
    end_hint = State()
    right_answer = State()
    wrong_answer = State()
    confirm = State()
