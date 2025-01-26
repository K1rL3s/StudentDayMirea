from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Multiselect
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.client.cart.states import CartStates
from core.ids import ProductId, UserId
from core.services.purchases import PurchasesService


async def on_cart_item_selected(
    _: CallbackQuery,
    multi_select: Multiselect,
    dialog_manager: DialogManager,
    __: int,
) -> None:
    dialog_manager.dialog_data["selected"] = multi_select.get_checked()  # ??


@inject
async def on_refund_cart_confirm(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    purhcases_service: FromDishka[PurchasesService],
) -> None:
    selected_purchases: list[ProductId] = dialog_manager.dialog_data["selected"]
    user_id: UserId = dialog_manager.middleware_data["user_id"]

    await purhcases_service.refund(user_id, selected_purchases)

    await dialog_manager.start(state=CartStates.view)
