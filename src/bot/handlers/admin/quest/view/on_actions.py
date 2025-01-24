from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import QuestId, TgId
from core.services.qrcode_saver import QRCodeSaver
from core.services.quests import QuestsService
from database.models import UserModel
from database.repos.quests import QuestsRepo

from ..create.states import CreateQuestStates
from ..edit.states import EditQuestStates
from .states import AdminViewQuestsStates


@inject
async def on_quest_selected(
    callback: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    item_id: str,
    quests_repo: FromDishka[QuestsRepo],
) -> None:
    quest_id = dialog_manager.dialog_data["quest_id"] = QuestId(item_id)

    quest = await quests_repo.get_by_id(quest_id)
    if quest.image_id:
        caption = f"Задание «{quest.title}»"
        await callback.message.answer_photo(quest.image_id, caption)
        show_mode = ShowMode.DELETE_AND_SEND
    else:
        show_mode = None

    await dialog_manager.next(show_mode=show_mode)


async def on_create_quest(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=CreateQuestStates.order)


async def on_edit_reward(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]
    await dialog_manager.start(
        state=EditQuestStates.reward,
        data={"quest_id": quest_id},
    )


@inject
async def on_view_qrcode(
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
    quests_repo: FromDishka[QuestsRepo],
    qrcode_saver: FromDishka[QRCodeSaver],
) -> None:
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]
    text = f"Задание, ID: <code>{quest_id}</code>"

    quest = await quests_repo.get_by_id(quest_id)
    if quest.qrcode_image_id:
        await callback.message.answer_photo(photo=quest.qrcode_image_id, caption=text)
    else:
        await qrcode_saver.quest(text, quest.id, TgId(callback.from_user.id))

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND


@inject
async def on_confirm_delete_quest(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    quests_service: FromDishka[QuestsService],
) -> None:
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]
    master: UserModel = dialog_manager.middleware_data["user"]
    await quests_service.delete(quest_id, master.id)
    await dialog_manager.start(state=AdminViewQuestsStates.list)
