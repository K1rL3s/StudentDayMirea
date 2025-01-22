from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.translate import translate_role
from core.ids import UserId
from database.repos.tickets import TicketsRepo
from database.repos.users import UsersRepo


@inject
async def get_view_user_info(
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
    tickets_repo: FromDishka[TicketsRepo],
    **__: Any,
) -> dict[str, Any]:
    view_user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    user = await users_repo.get_by_id(view_user_id)
    ticket = await tickets_repo.get_by_user_id(view_user_id)
    role = translate_role(user.role, "Пользователь")
    lottery_ticket = str(ticket.id) if ticket else "не участвует"
    return {"view_user": user, "role": role, "lottery_ticket": lottery_ticket}
