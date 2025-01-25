from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.coupons.view.states import ViewCouponsStates
from core.ids import UserId
from core.services.coupons import CouponsService


async def coupon_description_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    description = message.text.strip()[:256]
    dialog_manager.dialog_data["description"] = description
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


@inject
async def confirm_create_coupon(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    coupons_service: FromDishka[CouponsService],
) -> None:
    description: str = dialog_manager.dialog_data["description"]
    creator_id: UserId = dialog_manager.middleware_data["user_id"]

    coupon_id = await coupons_service.create(description, creator_id)

    dialog_manager.dialog_data["coupon_id"] = coupon_id
    await dialog_manager.start(
        state=ViewCouponsStates.one,
        data={"coupon_id": coupon_id},
    )
