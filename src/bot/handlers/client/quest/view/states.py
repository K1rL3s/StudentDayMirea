from aiogram.fsm.state import State, StatesGroup


class ViewQuestsStates(StatesGroup):
    list = State()
    one = State()
