from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.users.view.states import ViewUserStates
from core.ids import TicketId, UserId
from core.services.tickets import TicketsService
from database.repos.tickets import TicketsRepo


@inject
async def ticket_id_input_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    tickets_repo: FromDishka[TicketsRepo],
) -> None:
    ticket_id = message.text.strip()
    if not ticket_id.isdigit():
        text = "Номер билета должен быть числом"
        await message.answer(text=text)
        return

    ticket_id = TicketId(int(ticket_id))
    if ticket := await tickets_repo.get_by_id(ticket_id):
        text = f"Такой номер билета уже занят: {ticket.user_id} {ticket.fio}"
        await message.answer(text=text)
        return

    dialog_manager.dialog_data["ticket_id"] = ticket_id
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


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
    ticket_id: TicketId = dialog_manager.dialog_data["ticket_id"]
    view_user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    fio: str = dialog_manager.dialog_data["fio"]
    group = message.text.strip()[:32]

    master_id: UserId = dialog_manager.middleware_data["user_id"]

    await tickets_service.create(ticket_id, view_user_id, fio, group, master_id)

    await dialog_manager.start(ViewUserStates.one, data={"view_user_id": view_user_id})
