from aiogram.fsm.state import State, StatesGroup


class CreateCouponStates(StatesGroup):
    phrase = State()
    reward = State()
    activation_limit = State()
    confirm = State()
