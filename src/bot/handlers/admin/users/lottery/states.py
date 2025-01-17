from aiogram.fsm.state import State, StatesGroup


class LotteryUserStates(StatesGroup):
    ticket_id = State()
    fio = State()
    group = State()
