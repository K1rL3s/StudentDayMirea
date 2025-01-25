from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from database.repos.tickets import TicketsRepo


@inject
async def get_lottery_info(
    tickets_repo: FromDishka[TicketsRepo],
    **__: Any,
) -> dict[str, Any]:
    tickets = await tickets_repo.get_all()
    return {"total_tickets": len(tickets)}
