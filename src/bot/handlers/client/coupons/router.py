from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.enums import SlashCommand
from core.exceptions import CouponAlreadyClaimed, NoFreeCoupons, WrongCouponAnswer
from core.ids import UserId
from core.services.coupons import CouponsService

from .states import CouponStates

router = Router(name=__file__)


@router.message(Command(SlashCommand.COUPON))
async def check_coupon_handler(
    message: Message,
    command: CommandObject,
    user_id: UserId,
    dialog_manager: DialogManager,
    coupons_service: FromDishka[CouponsService],
) -> None:
    if command.args is None or not command.args.strip():
        return None

    coupon_phrase = command.args.strip()
    try:
        coupon_id = await coupons_service.reward(user_id, coupon_phrase)
    except NoFreeCoupons:
        return await dialog_manager.start(state=CouponStates.no_free)
    except (WrongCouponAnswer, CouponAlreadyClaimed):
        return None

    await dialog_manager.start(state=CouponStates.view, data={"coupon_id": coupon_id})
    return None
