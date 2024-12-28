import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.dialogs.on_actions import on_go_to_admin_panel
from core.services.broadcast import Broadcaster

MAX_MESSAGE_LEN = 1024 * 3


async def on_input_broadcast_message(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data["broadcast_message"] = message.html_text[
        :MAX_MESSAGE_LEN
    ]
    await dialog_manager.next()


@inject
async def start_broadcast(
    callback: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    broadcaster: FromDishka[Broadcaster],
) -> None:
    await callback.answer("⏳ Рассылка началась!", show_alert=True)

    broadcast_message = dialog_manager.dialog_data["broadcast_message"]
    result = await broadcaster.broadcast(callback.bot, broadcast_message)
    logging.info(
        "Broadcast from %d: ok=%d fail=%d",
        callback.from_user.id,
        result.ok,
        result.fail,
    )

    await on_go_to_admin_panel(callback, __, dialog_manager)
