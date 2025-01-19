from aiogram.fsm.state import State, StatesGroup


class AdminViewQuestsStates(StatesGroup):
    list = State()
    one = State()
    confirm = State()
