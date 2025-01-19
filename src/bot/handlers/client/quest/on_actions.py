from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from core.ids import QuestId

from .view.states import ViewQuestsStates


async def on_back_to_quest(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    quest_id: QuestId = dialog_manager.dialog_data["quest_id"]
    await dialog_manager.start(ViewQuestsStates.one, data={"quest_id": quest_id})
