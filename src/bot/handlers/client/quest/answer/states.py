from aiogram.fsm.state import State, StatesGroup


class AnswerQuestStates(StatesGroup):
    wait = State()
    ok = State()
    fail = State()
