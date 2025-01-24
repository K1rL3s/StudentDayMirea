from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.translate import translate_role
from database.models import UserModel
from database.repos.users import UsersRepo


async def get_user_info(
    dialog_manager: DialogManager,
    **__: Any,
) -> dict[str, Any]:
    user: UserModel = dialog_manager.middleware_data["user"]
    return {
        "role": translate_role(user.role),
    }


@inject
async def get_users_count(
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
    **__: Any,
) -> dict[str, Any]:
    active_users = await users_repo.get_active()
    all_users = await users_repo.get_all()
    return {"active_users": len(active_users), "all_users": len(all_users)}
