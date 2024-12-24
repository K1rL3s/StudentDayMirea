import re

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.client.start.states import StartStates
from bot.stickers import PANDA_NICE
from core.enums import RightsRole
from database.repos.users import UsersRepo

SUCCESS_TEXT = """
Вы успешно зарегистрировались! 🎉\n\n<b>Ваш id: <code>{user_id}</code></b>

Теперь вы можете вызывать <b>меню</b> командой <i>/menu</i>
""".strip()


async def name_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data["retry"] = True

    full_name = message.text.strip()
    if not re.match(r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$", full_name):
        return

    manager.dialog_data["full_name"] = full_name
    await manager.next()


@inject
async def register_confirm(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    user_id = callback.from_user.id
    full_name = manager.dialog_data["full_name"]
    owner_id: int = manager.middleware_data["owner_id"]

    role = RightsRole.ADMIN if user_id == owner_id else None
    await users_repo.update(user_id, full_name, role)

    await callback.message.answer_sticker(PANDA_NICE)
    await callback.message.answer(text=SUCCESS_TEXT.format(user_id=user_id))
    await manager.done()


async def register_disconfirm(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(
        state=StartStates.name,
        data={"retry": True},
    )
