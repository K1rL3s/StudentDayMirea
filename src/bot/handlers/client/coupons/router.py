from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.dialogs.flags import FORCE_GET_USER_KEY
from bot.enums import SlashCommand
from core.exceptions import CouponAlreadyClaimed, NoFreeCoupons, WrongCouponAnswer
from core.ids import UserId
from core.services.coupons import CouponsService
from database.repos.coupons import CouponsRepo

from ..menu.states import MenuStates
from .states import CouponStates

router = Router(name=__file__)


@router.message(Command(SlashCommand.COUPON))
async def check_coupon_handler(
    message: Message,
    command: CommandObject,
    user_id: UserId,
    dialog_manager: DialogManager,
    coupons_repo: FromDishka[CouponsRepo],
    coupons_service: FromDishka[CouponsService],
) -> None:
    if command.args is None or not command.args.strip():
        return None

    coupon_phrase = command.args.strip()
    try:
        await coupons_service.reward(user_id, coupon_phrase)
    except NoFreeCoupons:
        return await dialog_manager.start(state=CouponStates.no_free)
    except (WrongCouponAnswer, CouponAlreadyClaimed):
        return None

    """
    Ты получил промокод на скидку 200 рублей на 1 заказ от 700 рублей: 
    """

    coupon = await coupons_repo.get_by_user_id(user_id)
    text = (
        "🛴 Ты получил промокод от самоката "
        "на скидку 200 рублей на 1 заказ от 700 рублей: "
        f"<b>{coupon.description}</b>\n\n"
        "Действие промокода с 29.01 по 1.03"
    )
    await message.answer(text=text)

    await dialog_manager.start(state=MenuStates.menu, data={FORCE_GET_USER_KEY: None})
    return None
