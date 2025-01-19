from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import UserId
from core.services.qrcode_saver import QRCodeSaver
from database.repos.users import UsersRepo

from ..cart.states import CartUserStates
from ..lottery.states import LotteryUserStates
from ..role.states import RoleUserStates
from ..task.view.states import TaskUserStates


@inject
async def id_input_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    user_id = int(message.text)

    user = await users_repo.get_by_id(user_id)
    if user is None:
        text = f"Пользователя с ID {user_id} не существует :("
        await message.reply(text=text)
        return

    dialog_manager.dialog_data["view_user_id"] = user.id
    await dialog_manager.next()


@inject
async def on_check_cart(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    await dialog_manager.start(
        state=CartUserStates.cart,
        data={"view_user_id": user_id},
    )


async def on_set_role(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    await dialog_manager.start(
        state=RoleUserStates.select,
        data={"view_user_id": user_id},
    )


@inject
async def on_view_qrcode(
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
    qrcode_saver: FromDishka[QRCodeSaver],
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    user = await users_repo.get_by_id(user_id)
    text = f"Юзер, ID: <code>{user.id}</code>"
    if user.qrcode_image_id:
        await callback.message.answer_photo(photo=user.qrcode_image_id, caption=text)
    else:
        await qrcode_saver.user(text, user.id, callback.from_user.id)

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND


async def on_view_role(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    await dialog_manager.start(
        state=RoleUserStates.role,
        data={"view_user_id": user_id},
    )


async def on_view_task(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    await dialog_manager.start(TaskUserStates.task, data={"view_user_id": user_id})


async def on_set_lottery_info(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    await dialog_manager.start(
        LotteryUserStates.ticket_id,
        data={"view_user_id": user_id},
    )
