from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.filters.roles import IsAdmin
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToSecretsButton
from ..getters import get_all_secrets, get_one_secret
from .on_actions import (
    on_confirm_delete_secret,
    on_create_secret,
    on_delete_secret,
    on_secret_selected,
)
from .states import ViewSecretsStates

secrets_list_window = Window(
    Const("🤫 Все секреты"),
    ScrollingGroup(
        Select(
            Format("{item.id} | {item.phrase}"),
            id="secrets_select",
            items="secrets",
            on_click=on_secret_selected,
            item_id_getter=lambda item: item.id,
            type_factory=int,
        ),
        width=1,
        height=10,
        hide_on_single_page=True,
        id="secrets_group",
    ),
    Button(
        Const("✏️ Создать секрет"),
        id="create",
        on_click=on_create_secret,
        when=IsAdmin(),
    ),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_all_secrets,
    state=ViewSecretsStates.list,
)

view_one_secret_window = Window(
    Format(
        "id={secret.id}\n"
        "phrase={secret.phrase}\n"
        "reward={secret.reward}\n"
        "activation_limit={secret.activation_limit}\n"
        "total_activations={total_activations}",
    ),
    Button(
        Const("🗑️ Удалить"),
        id="delete",
        on_click=on_delete_secret,
        when=IsAdmin(),
    ),
    Back(Const("⏪ Cекреты")),
    GoToAdminPanelButton(),
    getter=get_one_secret,
    state=ViewSecretsStates.one,
)

confirm_delete_secret_window = Window(
    Format("❓ Вы уверены, что хотите удалить секрет id={secret.id}? "),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_delete",
        on_click=on_confirm_delete_secret,
    ),
    Back(Const("⏪ Отмена")),
    GoToSecretsButton(),
    GoToAdminPanelButton(),
    getter=get_one_secret,
    state=ViewSecretsStates.confirm,
)

view_secrets_dialog = Dialog(
    secrets_list_window,
    view_one_secret_window,
    confirm_delete_secret_window,
    on_start=on_start_update_dialog_data,
)
