from aiogram import F, Router
from aiogram.filters import CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from core.services.qrcodes import TaskIdPrefix
from database.repos.tasks import TasksRepo

from .view.states import ViewTasksStates

router = Router(name=__file__)


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith(TaskIdPrefix)),
    MagicData(F.command.args.as_("task_deeplink")),
)
async def start_task_by_deeplink(
    message: Message,
    task_deeplink: str,
    dialog_manager: DialogManager,
    task_repo: FromDishka[TasksRepo],
) -> None:
    task_id = task_deeplink.lstrip(TaskIdPrefix)

    if await task_repo.get_by_id(task_id):
        await dialog_manager.start(ViewTasksStates.one, data={"task_id": task_id})
