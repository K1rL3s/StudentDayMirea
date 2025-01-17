import re

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.stickers import PANDA_NICE
from core.enums import RightsRole
from core.ids import UserId
from database.repos.users import UsersRepo

from ..menu.states import MenuStates
from .states import StartStates

SUCCESS_TEXT = """
Вы успешно зарегистрировались! 🎉\n\n<b>Ваш id: <code>{user_id}</code></b>
""".strip()


async def name_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data["retry"] = True

    full_name = message.text.strip()
    if not re.match(r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$", full_name):
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
    bot_owner_id: UserId = dialog_manager.middleware_data["owner_id"]
    user_id: UserId = dialog_manager.middleware_data["user_id"]

    role = RightsRole.ADMIN if tg_id == bot_owner_id else None
    await users_repo.update(user_id, full_name, role)

    await callback.message.answer_sticker(PANDA_NICE)
    await callback.message.answer(text=SUCCESS_TEXT.format(user_id=user_id))
    await dialog_manager.start(state=MenuStates.menu)


async def register_disconfirm(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=StartStates.name, data={"retry": True})
