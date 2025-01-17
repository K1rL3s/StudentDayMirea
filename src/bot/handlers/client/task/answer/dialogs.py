from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton, GoToTaskButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import get_active_task
from .on_actions import on_answer_input
from .states import AnswerTaskStates

wait_answer_window = Window(
    Const("⏳ Введите ответ на задание ⬇"),
    MessageInput(
        func=on_answer_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    GoToTaskButton(),
    GoToMenuButton(),
    state=AnswerTaskStates.wait,
)

ok_answer_window = Window(
    Const("🎉 Верно!"),
    Format("Вы получили {start_data[reward]} Пятаков за задание «{start_data[title]}»"),
    GoToMenuButton(),
    state=AnswerTaskStates.ok,
)


fail_answer_window = Window(
    Const("😢 Не правильно..."),
    Const("Попробуйте ещё раз"),
    GoToTaskButton(),
    GoToMenuButton(),
    getter=get_active_task,
    state=AnswerTaskStates.fail,
)


task_answer_dialog = Dialog(
    wait_answer_window,
    ok_answer_window,
    fail_answer_window,
    on_start=on_start_update_dialog_data,
)
