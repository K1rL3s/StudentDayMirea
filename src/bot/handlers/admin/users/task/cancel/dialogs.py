from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ...on_actions import on_go_view_user
from ..on_actions import on_go_user_task
from .on_actions import on_cancel_task
from .states import CancelTaskStates

cancel_task_window = Window(
    Const("Вы уверены, что хотите прекратить выполнение задания❓"),
    Button(Const("✅ Подтвердить"), id="confirm", on_click=on_cancel_task),
    Button(Const("⏪ Задание"), id="task", on_click=on_go_user_task),
    Button(Const("⏪ Юзер"), id="user", on_click=on_go_view_user),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    state=CancelTaskStates.cancel,
)

cancel_task_dialog = Dialog(cancel_task_window, on_start=on_start_update_dialog_data)
