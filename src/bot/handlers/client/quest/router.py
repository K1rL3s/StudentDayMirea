from aiogram import F, Router
from aiogram.filters import Command, CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.enums import SlashCommand
from core.exceptions import QuestNotFound
from core.final_quest import FINAL_QUEST_ID
from core.ids import QuestId, UserId
from core.services.qrcodes import QuestIdPrefix
from core.services.quests import QuestsService
from database.repos.quests import QuestsRepo

from .view.states import ViewQuestsStates

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
    quest_id = QuestId(quest_deeplink[len(QuestIdPrefix):])
    if quest_id == FINAL_QUEST_ID:
        return

    try:
        quest = await quests_service.start(quest_id, user_id)
    except QuestNotFound:
        return

    if quest.image_id:
        caption = f"Задание «{quest.title}»"
        await message.answer_photo(quest.image_id, caption)

    await dialog_manager.start(ViewQuestsStates.one, data={"quest_id": quest_id})


@router.message(Command(SlashCommand.QUEST))
async def view_quest(
    message: Message,
    user_id: UserId,
    dialog_manager: DialogManager,
    quests_repo: FromDishka[QuestsRepo],
) -> None:
    if await quests_repo.get_known_quests(user_id):
        await dialog_manager.start(state=ViewQuestsStates.list)
