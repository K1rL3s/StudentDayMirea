from aiogram.fsm.state import State, StatesGroup


class CartStates(StatesGroup):
    view = State()
    refund = State()
