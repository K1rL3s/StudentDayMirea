from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.dialogs.flags import FORCE_GET_USER_KEY
from bot.handlers.client.menu.states import MenuStates
from core.ids import UserId
from core.services.broadcast import Broadcaster
from core.services.users import UsersService
from database.models import UserModel
from database.repos.users import UsersRepo


@inject
async def id_input_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    receiver_id = int(message.text)
    user_id: UserId = dialog_manager.middleware_data["user_id"]

    if receiver_id == user_id:
        text = "😢  Нельзя сделать перевод самому себе"
        await message.answer(text=text)
        return

    receiver = await users_repo.get_by_id(receiver_id)
    if receiver is None:
        text = f"😢 Пользователя с ID {receiver_id} не существует"
        await message.answer(text=text)
        return

    dialog_manager.dialog_data["receiver_id"] = receiver.id
    dialog_manager.dialog_data["receiver_name"] = receiver.name
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


@inject
async def amount_input_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    users_service: FromDishka[UsersService],
    users_repo: FromDishka[UsersRepo],
    broadcaster: FromDishka[Broadcaster],
) -> None:
    amount = int(message.text.strip())
    user: UserModel = dialog_manager.middleware_data["user"]

    if user.balance < amount:
        text = "😢 У вас недостаточно Пятаков для перевода, введите другую сумму"
        await message.answer(text=text)
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
        return

    receiver_id: UserId = dialog_manager.dialog_data["receiver_id"]
    await users_service.transfer_funds(user.id, receiver_id, int(amount))

    text = f"💵 Вам перевели {amount} Пятаков!"
    receiver = await users_repo.get_by_id(receiver_id)
    await broadcaster.one_notify(text=text, user_id=receiver_id, tg_id=receiver.tg_id)

    text = "💵 Перевод прошёл успешно!"
    await broadcaster.one_notify(text=text, user_id=user.id, tg_id=user.tg_id)

    await dialog_manager.start(
        state=MenuStates.menu,
        data={FORCE_GET_USER_KEY: True},
    )
