from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.client.menu.states import MenuStates
from core.ids import QuestId, UserId
from database.repos.quests import QuestsRepo

from ..answer.states import AnswerQuestStates


@inject
async def on_quest_selected(
    callback: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    item_id: str,
    quests_repo: FromDishka[QuestsRepo],
) -> None:
    quest_id = dialog_manager.dialog_data["quest_id"] = item_id

    quest = await quests_repo.get_by_id(quest_id)
    if quest.image_id:
        caption = f"Задание «{quest.title}»"
        await callback.message.answer_photo(quest.image_id, caption)
        show_mode = ShowMode.DELETE_AND_SEND
    else:
        show_mode = None

    await dialog_manager.next(show_mode=show_mode)


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
