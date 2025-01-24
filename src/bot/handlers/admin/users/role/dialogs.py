from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Group, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToUserButton
from ..getters import get_view_user_info
from ..on_actions import _UserIdNameText
from .getters import get_roles
from .on_actions import on_role_confirm, on_role_selected
from .states import RoleUserStates

user_role_window = Window(
    _UserIdNameText,
    Group(
        Select(
            Format("{item[1]}"),
            id="select_roles",
            item_id_getter=lambda item: item[0],
            items="roles",
            type_factory=int,
            on_click=on_role_selected,
        ),
        width=2,
    ),
    GoToUserButton,
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=[get_view_user_info, get_roles],
    state=RoleUserStates.select,
)

set_role_window = Window(
    Format(
        '❓ Уверен, что хочешь установить роль "{dialog_data[role_name]}" '
        "пользователю {view_user.id} - {view_user.name}?",
    ),
    Button(Const("✅ Подтвердить"), id="confirm", on_click=on_role_confirm),
    Back(Const("⏪ Роли")),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_view_user_info,
    state=RoleUserStates.role,
)

user_role_dialog = Dialog(
    user_role_window,
    set_role_window,
    on_start=on_start_update_dialog_data,
)
