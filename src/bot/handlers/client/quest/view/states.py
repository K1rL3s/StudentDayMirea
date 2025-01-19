from aiogram.fsm.state import State, StatesGroup


class ViewQuestStates(StatesGroup):
    list = State()
    one = State()
