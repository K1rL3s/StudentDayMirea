from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from core.ids import QuestId

from .view.states import AdminViewQuestsStates


class GoToQuestsButton(Button):
    def __init__(self, text: str = "🗺️ Квест", **kwargs: Any) -> None:
        super().__init__(
            text=Const(text),
            id="to_quests",
            on_click=self._on_go_to_quests,
            **kwargs,
        )

    @staticmethod
    async def _on_go_to_quests(
        _: CallbackQuery,
        __: Button,
        dialog_manager: DialogManager,
    ) -> None:
        await dialog_manager.start(state=AdminViewQuestsStates.list)


class GoToQuestButton(Button):
    def __init__(self, text: str = "⏪ Задание", **kwargs: Any) -> None:
        super().__init__(
            text=Const(text),
            id="to_quest",
            on_click=self._on_go_to_quest,
            **kwargs,
        )

    @staticmethod
    async def _on_go_to_quest(
        _: CallbackQuery,
        __: Button,
        dialog_manager: DialogManager,
    ) -> None:
        quest_id: QuestId = dialog_manager.dialog_data["quest_id"]
        await dialog_manager.start(
            state=AdminViewQuestsStates.one,
            data={"quest_id": quest_id},
        )
