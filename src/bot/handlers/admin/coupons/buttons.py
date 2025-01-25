from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from .view.states import ViewCouponsStates


class GoToCouponsButton(Button):
    def __init__(self, text: str = "🛴 Купоны", **kwargs: Any) -> None:
        super().__init__(
            text=Const(text),
            id="to_coupons",
            on_click=self._on_go_to_coupons,
            **kwargs,
        )

    @staticmethod
    async def _on_go_to_coupons(
        _: CallbackQuery,
        __: Button,
        dialog_manager: DialogManager,
    ) -> None:
        await dialog_manager.start(state=ViewCouponsStates.list)
