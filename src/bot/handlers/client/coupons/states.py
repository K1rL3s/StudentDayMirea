from aiogram.fsm.state import State, StatesGroup


class CouponStates(StatesGroup):
    view = State()
    no_free = State()
