from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Multiselect
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.panel.states import AdminPanelStates
from core.ids import ProductId, UserId
from core.services.purchases import PurchasesService
from database.models import UserModel


async def on_cart_item_selected(
    _: CallbackQuery,
    multi_select: Multiselect,
    dialog_manager: DialogManager,
    __: int,
) -> None:
    dialog_manager.dialog_data["selected"] = multi_select.get_checked()  # ??


@inject
async def on_clear_cart_confirm(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    purhcases_service: FromDishka[PurchasesService],
) -> None:
    selected_purchases: list[ProductId] = dialog_manager.dialog_data["selected"]
    view_user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    admin: UserModel = dialog_manager.middleware_data["user"]

    await purhcases_service.clear_cart(view_user_id, selected_purchases, admin.id)

    await dialog_manager.start(state=AdminPanelStates.panel)
