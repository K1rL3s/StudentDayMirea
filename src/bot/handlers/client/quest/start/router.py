from aiogram import F, Router
from aiogram.filters import CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from core.exceptions import QuestNotFound
from core.ids import UserId
from core.services.qrcodes import QuestIdPrefix
from core.services.quests import QuestsService

from ..view.states import ViewQuestStates

router = Router(name=__file__)


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith(QuestIdPrefix)),
    MagicData(F.command.args.as_("quest_deeplink")),
)
async def start_quest_by_deeplink(
    message: Message,
    quest_deeplink: str,
    user_id: UserId,
    dialog_manager: DialogManager,
    quests_service: FromDishka[QuestsService],
) -> None:
    quest_id = quest_deeplink.lstrip(QuestIdPrefix)
    try:
        await quests_service.start(quest_id, user_id)
    except QuestNotFound:
        return

    await dialog_manager.start(ViewQuestStates.one, data={"quest_id": quest_id})
