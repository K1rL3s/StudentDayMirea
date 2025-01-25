from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.panel.states import AdminPanelStates
from core.ids import UserId
from core.services.tickets import TicketsService


async def fio_input_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    fio = message.text.strip()[:256]
    dialog_manager.dialog_data["fio"] = fio
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


@inject
async def group_input_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    tickets_service: FromDishka[TicketsService],
) -> None:
    view_user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    fio: str = dialog_manager.dialog_data["fio"]
    group = message.text.strip()[:32]

    master_id: UserId = dialog_manager.middleware_data["user_id"]

    await tickets_service.create_or_update(view_user_id, fio, group, master_id)

    await dialog_manager.start(state=AdminPanelStates.panel)
