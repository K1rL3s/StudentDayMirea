from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format

from core.ids import UserId

from .view.states import ViewUserStates

_UserIdNameText = Format(
    "ID: <code>{view_user.id}</code>\n"
    "<b>{view_user.name}</b> - {role}\n"
    "Лотерейный билет - {lottery_ticket}",
)


async def on_go_view_user(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    await dialog_manager.start(state=ViewUserStates.one, data={"view_user_id": user_id})
