from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import get_quest_by_id
from ..on_actions import on_back_to_quest
from .on_actions import on_answer_input
from .states import AnswerQuestStates

wait_answer_window = Window(
    Const("⏳ Введите ответ на задание ⬇"),
    MessageInput(
        func=on_answer_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Button(Const("⏪ Записка"), id="quest", on_click=on_back_to_quest),
    GoToMenuButton(),
    state=AnswerQuestStates.wait,
)

ok_answer_window = Window(
    Const("🎉 Верно!"),
    Format("Вы получили {quest.reward} Пятаков за задание «{quest.title}»\n"),
    Format("💡 {quest.end_hint}", when=F["quest"].end_hint),
    GoToMenuButton(),
    getter=get_quest_by_id,
    state=AnswerQuestStates.ok,
)

fail_answer_window = Window(
    Const("😢 Не правильно..."),
    Const("Попробуйте ещё раз"),
    Button(Const("⏪ Записка"), id="quest", on_click=on_back_to_quest),
    GoToMenuButton(),
    state=AnswerQuestStates.fail,
)

quest_answer_dialog = Dialog(
    wait_answer_window,
    ok_answer_window,
    fail_answer_window,
    on_start=on_start_update_dialog_data,
)
