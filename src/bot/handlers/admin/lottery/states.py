from aiogram.fsm.state import State, StatesGroup


class LotteryStartInputStates(StatesGroup):
    user_id = State()
