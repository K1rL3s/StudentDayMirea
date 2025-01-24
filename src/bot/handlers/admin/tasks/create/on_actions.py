from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.tasks.view.states import ViewTasksStates
from core.ids import UserId
from core.services.tasks import TasksService


async def task_title_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    title = message.text.strip()[:256]
    dialog_manager.dialog_data["title"] = title
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def task_description_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    description = message.html_text.strip()[:2048]
    dialog_manager.dialog_data["description"] = description
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def task_reward_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    reward = int(message.text)
    dialog_manager.dialog_data["reward"] = reward
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def task_answer_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    answer = message.text.strip()[:256]
    dialog_manager.dialog_data["answer"] = answer.casefold()
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


@inject
async def confirm_create_task(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    tasks_service: FromDishka[TasksService],
) -> None:
    title: str = dialog_manager.dialog_data["title"]
    description: str = dialog_manager.dialog_data["description"]
    reward: int = dialog_manager.dialog_data["reward"]
    answer: str = dialog_manager.dialog_data["answer"]
    creator_id: UserId = dialog_manager.middleware_data["user_id"]

    task_id = await tasks_service.create(
        title,
        description,
        reward,
        answer,
        creator_id,
    )

    await dialog_manager.start(state=ViewTasksStates.one, data={"task_id": task_id})
