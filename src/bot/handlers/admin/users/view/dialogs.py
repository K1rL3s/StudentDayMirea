from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Group
from aiogram_dialog.widgets.text import Const

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.filters.roles import IsAdmin, IsLottery, IsSeller, IsStager
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import get_view_user_info
from ..on_actions import UserAdminInfoText
from .on_actions import (
    id_input_handler,
    on_check_cart,
    on_set_lottery_info,
    on_set_role,
    on_view_qrcode,
    on_view_task,
)
from .states import ViewUserStates

wait_user_id_window = Window(
    Const("🆔 Введи ID человека, которого хочешь увидеть"),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    MessageInput(
        id_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),  # ok
    ),
    state=ViewUserStates.id,
)

view_user_window = Window(
    UserAdminInfoText,
    Group(
        Button(
            Const("🧺 Корзина"),
            id="cart",
            on_click=on_check_cart,
            when=IsSeller(),
        ),
        Button(
            Const("🧠 Задание"),
            id="task",
            on_click=on_view_task,
            when=IsStager(),
        ),
        Button(
            Const("👨‍💼 Выдать роль"),
            id="role",
            on_click=on_set_role,
            when=IsAdmin(),
        ),
        Button(
            Const("🎟️ Лотерея"),
            id="lottery",
            on_click=on_set_lottery_info,
            when=IsLottery(),
        ),
        Button(
            Const("🖼️ Куркод юзера"),
            id="qrcode",
            on_click=on_view_qrcode,
        ),
        width=2,
    ),
    Back(Const("🔁 Ввести ID")),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_view_user_info,
    state=ViewUserStates.one,
)

view_user_dialog = Dialog(
    wait_user_id_window,
    view_user_window,
    on_start=on_start_update_dialog_data,
)
