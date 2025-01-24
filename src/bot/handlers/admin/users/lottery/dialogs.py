from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.text import Const

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToUserButton
from ..getters import get_view_user_info
from .on_actions import fio_input_handler, group_input_handler
from .states import LotteryUserStates

fio_window = Window(
    Const("👤 Введи ФИО"),
    MessageInput(
        fio_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    GoToUserButton,
    GoToAdminPanelButton(),
    GoToMenuButton(),
    state=LotteryUserStates.fio,
    getter=get_view_user_info,
)

group_window = Window(
    Const("🎓 Введи группу студента"),
    MessageInput(
        group_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    state=LotteryUserStates.group,
    getter=get_view_user_info,
)

set_lottery_info_dialog = Dialog(
    fio_window,
    group_window,
    on_start=on_start_update_dialog_data,
)
