from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.dialogs.flags import FORCE_GET_USER_KEY
from bot.translate import translate_role
from database.models import UserModel
from database.repos.tasks import TasksRepo
from database.repos.users import UsersRepo


@inject
async def get_user_info(
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
    tasks_repo: FromDishka[TasksRepo],
    **__: Any,
) -> dict[str, Any]:
    user: UserModel = dialog_manager.middleware_data["user"]
    if dialog_manager.start_data and FORCE_GET_USER_KEY in dialog_manager.start_data:
        user = await users_repo.get_by_id(user.id)
    task = await tasks_repo.get_active_task(user.id)

    return {
        "user_id": user.id,
        "balance": user.balance,
        "role": translate_role(user.role),
        "task": task,
    }
