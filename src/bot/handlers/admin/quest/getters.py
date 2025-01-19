from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import QuestId
from database.repos.quests import QuestsRepo


@inject
async def get_all_quests(
    quests_repo: FromDishka[QuestsRepo],
    **__: Any,
) -> dict[str, Any]:
    quests = await quests_repo.get_all()
    return {"quests": quests}


@inject
async def get_quest_by_id(
    dialog_manager: DialogManager,
    quests_repo: FromDishka[QuestsRepo],
    **__: Any,
) -> dict[str, Any]:
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]
    quest = await quests_repo.get_by_id(quest_id)
    return {"quest": quest}
