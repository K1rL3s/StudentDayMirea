from aiogram.fsm.state import State, StatesGroup


class ViewCouponsStates(StatesGroup):
    list = State()
    one = State()
    confirm = State()
