from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.coupons.create.states import CreateCouponStates
from bot.handlers.admin.coupons.view.states import ViewCouponsStates
from core.ids import CouponId
from core.services.coupons import CouponsService
from database.models import UserModel


async def on_coupon_selected(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    dialog_manager.dialog_data["coupon_id"] = item_id
    await dialog_manager.next()


async def on_create_coupon(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=CreateCouponStates.phrase)


async def on_delete_coupon(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.next()


@inject
async def on_confirm_delete_coupon(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    coupons_service: FromDishka[CouponsService],
) -> None:
    coupon_id: CouponId = dialog_manager.dialog_data["coupon_id"]
    admin: UserModel = dialog_manager.middleware_data["user"]
    await coupons_service.delete(coupon_id, admin.id)
    await dialog_manager.start(state=ViewCouponsStates.list)
