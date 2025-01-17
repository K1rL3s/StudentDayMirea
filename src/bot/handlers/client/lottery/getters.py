from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import UserId
from database.repos.tickets import TicketsRepo


@inject
async def get_lottery_info(
    dialog_manager: DialogManager,
    tickets_repo: FromDishka[TicketsRepo],
    **__: Any,
) -> dict[str, Any]:
    user_id: UserId = dialog_manager.middleware_data["user_id"]
    ticket = await tickets_repo.get_by_user_id(user_id)
    tickets = await tickets_repo.get_all()
    return {"total_tickets": len(tickets), "ticket_id": ticket.id if ticket else None}
