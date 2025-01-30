from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format, Multi

from core.ids import UserId

from .view.states import ViewUserStates

UserAdminInfoText = Multi(
    Format("ID: <code>{view_user.id}</code>"),
    Format("<b>{view_user.name}</b> - {role}"),
    Format('<a href="tg://openmessage?user_id={view_user.tg_id}">тык</a>'),
    Format('<a href="tg://user?id={view_user.tg_id}">тык</a>'),
    Format("Лотерея - {lottery}"),
    Format("ФИО - {fio}", when=F["fio"]),
    Format("Группа - {group}", when=F["group"]),
    Const(" "),
)


async def on_go_view_user(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    await dialog_manager.start(state=ViewUserStates.one, data={"view_user_id": user_id})
