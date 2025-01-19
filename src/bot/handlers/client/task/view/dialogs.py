from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import get_active_task
from .on_actions import on_answer
from .states import ViewTaskStates

view_task_window = Window(
    Format("{task.title}\n"),
    Format("{task.description}"),
    Button(Const("✏️ Ввести ответ"), id="answer", on_click=on_answer),
    GoToMenuButton(),
    getter=get_active_task,
    state=ViewTaskStates.task,
)


view_task_dialog = Dialog(
    view_task_window,
    on_start=on_start_update_dialog_data,
)
