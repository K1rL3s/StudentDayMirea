import re

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.dialogs.flags import FORCE_GET_USER_KEY
from core.enums import RightsRole
from core.ids import UserId
from database.repos.users import UsersRepo

from ..menu.states import MenuStates
from .states import StartStates


async def name_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    full_name = message.text.strip()
    if not re.match(r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$", full_name):
        dialog_manager.dialog_data["retry"] = "format"
        return

    dialog_manager.dialog_data["full_name"] = full_name
    await dialog_manager.next()


@inject
async def register_confirm(
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    tg_id = callback.from_user.id
    full_name = dialog_manager.dialog_data["full_name"]
    bot_owner_ids: list[UserId] = dialog_manager.middleware_data["owner_id"]
    user_id: UserId = dialog_manager.middleware_data["user_id"]

    role = RightsRole.ADMIN if tg_id in bot_owner_ids else None
    await users_repo.update(user_id, full_name, role)

    await dialog_manager.start(
        state=MenuStates.menu,
        data={FORCE_GET_USER_KEY: None},
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def register_disconfirm(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=StartStates.name, data={"retry": True})
