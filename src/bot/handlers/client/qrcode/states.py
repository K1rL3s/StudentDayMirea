from aiogram.fsm.state import State, StatesGroup


class ShowQrStates(StatesGroup):
    qr = State()
