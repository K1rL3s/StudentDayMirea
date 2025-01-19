from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format, Multi

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ...buttons import GoToUserButton
from ..getters import get_active_task
from .on_actions import on_cancel_task, on_confirm_task
from .states import TaskUserStates

view_task_window = Window(
    Const(
        "Нет активного задания",
        when=F["task"].is_(None),
    ),
    Multi(
        Format("{task.title}"),
        Format("{task.description}"),
        Format("{task.reward}"),
        when=F["task"].is_not(None),
        sep="\n\n",
    ),
    Button(
        Const("✅ Подтвердить"),
        id="confirm",
        on_click=on_confirm_task,
        when=F["task"].is_not(None),
    ),
    Button(
        Const("❌ Отменить"),
        id="cancel",
        on_click=on_cancel_task,
        when=F["task"].is_not(None),
    ),
    GoToUserButton,
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_active_task,
    state=TaskUserStates.task,
)

view_user_task_dialog = Dialog(view_task_window, on_start=on_start_update_dialog_data)
