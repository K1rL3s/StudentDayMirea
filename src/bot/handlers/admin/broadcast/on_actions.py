import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.dialogs.on_actions import on_go_to_admin_panel
from core.ids import UserId
from core.services.broadcast import Broadcaster

MAX_MESSAGE_LEN = 1024 * 3


async def on_input_broadcast_message(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    broadcast_message = message.html_text[:MAX_MESSAGE_LEN]
    dialog_manager.dialog_data["broadcast_message"] = broadcast_message
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


@inject
async def start_broadcast(
    callback: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    broadcaster: FromDishka[Broadcaster],
) -> None:
    await callback.answer("⏳ Рассылка началась!", show_alert=True)

    broadcast_message: str = dialog_manager.dialog_data["broadcast_message"]
    user_id: UserId = dialog_manager.middleware_data["user_id"]
    result = await broadcaster.broadcast(broadcast_message, user_id)
    logging.info(
        "Broadcast from %d: ok=%d fail=%d",
        user_id,
        result.ok,
        result.fail,
    )

    await on_go_to_admin_panel(callback, __, dialog_manager)
