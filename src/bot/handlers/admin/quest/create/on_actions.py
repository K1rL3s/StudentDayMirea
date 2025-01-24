from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import UserId
from core.services.quests import QuestsService

from ..view.states import AdminViewQuestsStates


async def quest_order_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    order = int(message.text)
    dialog_manager.dialog_data["order"] = order
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def quest_title_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    title = message.text.strip()[:256]
    dialog_manager.dialog_data["title"] = title
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def quest_description_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    description = message.html_text.strip()[:2048]
    dialog_manager.dialog_data["description"] = description
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def quest_task_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    task = message.html_text.strip()[:1024]
    dialog_manager.dialog_data["task"] = task
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def quest_image_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    image_id = message.photo[-1].file_id
    dialog_manager.dialog_data["image_id"] = image_id
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def quest_reward_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    reward = int(message.text)
    dialog_manager.dialog_data["reward"] = reward
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def quest_answer_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    answer = message.text.strip()[:256]
    dialog_manager.dialog_data["answer"] = answer.casefold()
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def quest_end_hint_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    end_hint = message.text.strip()[:256]
    dialog_manager.dialog_data["end_hint"] = end_hint
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


@inject
async def confirm_create_quest(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    quests_service: FromDishka[QuestsService],
) -> None:
    order: int = dialog_manager.dialog_data["order"]
    title: str = dialog_manager.dialog_data["title"]
    description: str = dialog_manager.dialog_data["description"]
    task: str = dialog_manager.dialog_data["task"]
    image_id: str | None = dialog_manager.dialog_data.get("image_id")
    reward: int = dialog_manager.dialog_data["reward"]
    answer: str = dialog_manager.dialog_data["answer"]
    end_hint: str = dialog_manager.dialog_data["end_hint"]
    master_id: UserId = dialog_manager.middleware_data["user_id"]

    quest_id = await quests_service.create(
        order,
        title,
        description,
        task,
        image_id,
        reward,
        answer,
        end_hint,
        master_id,
    )

    await dialog_manager.start(
        state=AdminViewQuestsStates.one,
        data={"quest_id": quest_id},
    )
