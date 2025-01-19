from tkinter import Button

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.client.menu.states import MenuStates
from core.ids import QuestId, UserId
from database.repos.quests import QuestsRepo

from ..answer.states import AnswerQuestStates


async def on_quest_selected(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    dialog_manager.dialog_data["quest_id"] = item_id
    await dialog_manager.next()


@inject
async def on_answer(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    quests_repo: FromDishka[QuestsRepo],
) -> None:
    user_id: UserId = dialog_manager.middleware_data["user_id"]
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]

    if await quests_repo.is_quest_reward_claimed(user_id, quest_id):
        await dialog_manager.start(MenuStates.menu)
    else:
        await dialog_manager.start(AnswerQuestStates.wait, data={"quest_id": quest_id})
