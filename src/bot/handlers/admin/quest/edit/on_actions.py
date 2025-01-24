from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.quest.view.states import AdminViewQuestsStates
from core.ids import QuestId
from database.repos.quests import QuestsRepo


@inject
async def on_edit_reward_input(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
    quests_repo: FromDishka[QuestsRepo],
) -> None:
    reward = int(message.text)
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]

    await quests_repo.update(quest_id, reward=reward)
    await dialog_manager.start(AdminViewQuestsStates.one, data={"quest_id": quest_id})


@inject
async def on_edit_image_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    quests_repo: FromDishka[QuestsRepo],
) -> None:
    image_id = message.photo[-1].file_id
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]
    await quests_repo.update(quest_id, image_id=image_id)
    await dialog_manager.start(AdminViewQuestsStates.one, data={"quest_id": quest_id})


@inject
async def on_edit_without_image_input(
    _: CallbackQuery,
    __: MessageInput,
    dialog_manager: DialogManager,
    quests_repo: FromDishka[QuestsRepo],
) -> None:
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]
    await quests_repo.update(quest_id, image_id=None)
    await dialog_manager.start(AdminViewQuestsStates.one, data={"quest_id": quest_id})
