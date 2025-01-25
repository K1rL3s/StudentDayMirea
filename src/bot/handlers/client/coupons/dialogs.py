from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from .getters import get_coupon
from .states import CouponStates

view_coupon_window = Window(
    Format("🛴 Ваш купон от самоката: <b>{coupon.description}</b>"),
    GoToMenuButton(),
    getter=get_coupon,
    state=CouponStates.view,
)

no_free_coupons_window = Window(
    Const("😢 К сожалению, купоны закончились."),
    GoToMenuButton(),
    state=CouponStates.no_free,
)

coupons_dialog = Dialog(
    view_coupon_window,
    no_free_coupons_window,
    on_start=on_start_update_dialog_data,
)
