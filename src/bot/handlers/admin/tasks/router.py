from aiogram import F, Router
from aiogram.filters import Command, CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.enums import SlashCommand
from bot.filters.roles import IsStager
from core.services.qrcodes import TaskIdPrefix
from database.repos.tasks import TasksRepo

from .view.states import ViewTasksStates

router = Router(name=__file__)


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith(TaskIdPrefix)),
    MagicData(F.command.args.as_("task_deeplink")),
    IsStager(),
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

    await message.delete()


@router.message(Command(SlashCommand.TASKS))
async def list_tasks_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=ViewTasksStates.list)
