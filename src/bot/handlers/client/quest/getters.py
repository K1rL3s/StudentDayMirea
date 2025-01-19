from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import QuestId, UserId
from database.models import QuestModel, UsersToQuestsModel
from database.repos.quests import QuestsRepo


@inject
async def get_all_known_quests(
    quests_repo: FromDishka[QuestsRepo],
    dialog_manager: DialogManager,
    **__: Any,
) -> dict[str, list[tuple[QuestModel, UsersToQuestsModel]]]:
    user_id: UserId = dialog_manager.middleware_data["user_id"]
    quests = await quests_repo.get_known_quests(user_id)

    # TODO нормально сделать финальное задание
    all_quests = await quests_repo.get_all()
    if len(quests) == len(all_quests) and all(pair[1].status for pair in quests):
        final = True
    else:
        final = False

    return {"quests": quests, "final": final}


@inject
async def get_quest_by_id(
    quests_repo: FromDishka[QuestsRepo],
    dialog_manager: DialogManager,
    **__: Any,
) -> dict[str, QuestModel]:
    user_id: UserId = dialog_manager.middleware_data["user_id"]
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]

    quest = await quests_repo.get_by_id(quest_id)
    relation = await quests_repo.get_user_to_quest(quest_id, user_id)
    return {"quest": quest, "status": relation.status}
