from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.exceptions import WrongQuestAnswer
from core.ids import QuestId, UserId
from core.services.quests import QuestsService

from ..answer.states import AnswerQuestStates


@inject
async def on_answer_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    quests_service: FromDishka[QuestsService],
) -> None:
    user_id: UserId = dialog_manager.middleware_data["user_id"]
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]
    try:
        title, reward = await quests_service.reward_for_quest_by_pharse(
            quest_id,
            user_id,
            message.text,
        )
    except WrongQuestAnswer:
        return await dialog_manager.start(
            AnswerQuestStates.fail,
            data={"quest_id": quest_id},
        )

    return await dialog_manager.start(
        AnswerQuestStates.ok,
        data={"reward": reward, "title": title, "quest_id": quest_id},
    )
