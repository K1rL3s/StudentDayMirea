from aiogram.fsm.state import State, StatesGroup


class EditSecretStates(StatesGroup):
    phrase = State()
    reward = State()
    activation_limit = State()
