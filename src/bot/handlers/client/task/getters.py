from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import TaskId
from database.models import UserModel
from database.repos.tasks import TasksRepo


@inject
async def get_task_by_id(
    dialog_manager: DialogManager,
    tasks_repo: FromDishka[TasksRepo],
    **__: Any,
) -> dict[str, Any]:
    task_id: TaskId = dialog_manager.dialog_data["task_id"]
    task = await tasks_repo.get_by_id(task_id)
    return {"task": task}


@inject
async def get_active_task(
    dialog_manager: DialogManager,
    tasks_repo: FromDishka[TasksRepo],
    **__: Any,
) -> dict[str, Any]:
    user: UserModel = dialog_manager.middleware_data["user"]
    task = await tasks_repo.get_active_task(user.id)
    return {"task": task}


@inject
async def get_active_task_key(
    dialog_manager: DialogManager,
    tasks_repo: FromDishka[TasksRepo],
    **__: Any,
) -> dict[str, Any]:
    user: UserModel = dialog_manager.middleware_data["user"]
    task = await tasks_repo.get_active_task(user.id)
    return {"active_task": task}
