from aiogram.fsm.state import State, StatesGroup


class EditProductStates(StatesGroup):
    price = State()
    stock = State()
