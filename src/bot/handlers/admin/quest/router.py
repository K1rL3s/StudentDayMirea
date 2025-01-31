from aiogram import F, Router
from aiogram.filters import CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from core.ids import QuestId
from core.services.qrcodes import QuestIdPrefix
from database.repos.quests import QuestsRepo

from .view.states import AdminViewQuestsStates

router = Router(name=__file__)


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith(QuestIdPrefix)),
    MagicData(F.command.args.as_("quest_deeplink")),
)
async def view_quest_by_deeplink(
    message: Message,
    quest_deeplink: str,
    dialog_manager: DialogManager,
    quest_repo: FromDishka[QuestsRepo],
) -> None:
    quest_id = QuestId(quest_deeplink[len(QuestIdPrefix):])

    if await quest_repo.get_by_id(quest_id):
        await dialog_manager.start(
            AdminViewQuestsStates.one,
            data={"quest_id": quest_id},
        )
