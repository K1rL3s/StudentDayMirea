from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.users.lottery.states import LotteryUserStates
from database.repos.users import UsersRepo


async def _user_not_found(message: Message) -> None:
    text = "😥 Такого пользователя нет..."
    await message.answer(text=text)


@inject
async def user_id_input_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    user_id = message.text.strip()
    if not user_id.isdigit():
        return await _user_not_found(message)

    user_id = int(user_id)
    user = await users_repo.get_by_id(user_id)
    if user is None:
        return await _user_not_found(message)

    return await dialog_manager.start(
        LotteryUserStates.ticket_id,
        data={"view_user_id": user_id},
    )
