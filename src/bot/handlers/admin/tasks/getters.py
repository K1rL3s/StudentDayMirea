from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import TaskId
from database.repos.tasks import TasksRepo


@inject
async def get_all_tasks(
    tasks_repo: FromDishka[TasksRepo],
    **__: Any,
) -> dict[str, Any]:
    tasks = await tasks_repo.get_all()
    return {"tasks": tasks}


@inject
async def get_task_by_id(
    dialog_manager: DialogManager,
    tasks_repo: FromDishka[TasksRepo],
    **__: Any,
) -> dict[str, Any]:
    task_id: TaskId = dialog_manager.dialog_data["task_id"]
    task = await tasks_repo.get_by_id(task_id)
    return {"task": task}
