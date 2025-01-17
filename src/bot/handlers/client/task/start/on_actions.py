from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import TaskId
from core.services.tasks import TasksService
from database.models import UserModel

from ..view.states import ViewTaskStates


@inject
async def on_start_task(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    tasks_service: FromDishka[TasksService],
) -> None:
    user: UserModel = dialog_manager.middleware_data["user"]
    task_id: TaskId = dialog_manager.dialog_data["task_id"]
    await tasks_service.start(task_id, user.id)
    await dialog_manager.start(ViewTaskStates.task)
