from aiogram.fsm.state import State, StatesGroup


class EditQuestStates(StatesGroup):
    reward = State()
    image = State()
