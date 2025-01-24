from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import get_active_task_key, get_task_by_id
from .on_actions import on_start_task
from .states import StartTaskStates

start_task_window = Window(
    Format("🧠 Ты хочешь начать задание «{task.title}»?\n"),
    Const(
        "❗ Если начнёшь его, то текущее незавершённое задание отменится",
        when=F["active_task"],
    ),
    Button(Const("✅ Начать"), id="start", on_click=on_start_task),
    GoToMenuButton(),
    getter=[get_task_by_id, get_active_task_key],
    state=StartTaskStates.wait,
)


start_task_dialog = Dialog(
    start_task_window,
    on_start=on_start_update_dialog_data,
)
