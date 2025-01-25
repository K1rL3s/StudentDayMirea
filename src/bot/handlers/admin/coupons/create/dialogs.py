from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton

from ..buttons import GoToCouponsButton
from .on_actions import confirm_create_coupon, coupon_description_input
from .states import CreateCouponStates

create_coupon_window = Window(
    Const("🛴 Введи купон"),
    MessageInput(
        func=coupon_description_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    GoToCouponsButton(),
    state=CreateCouponStates.phrase,
)

confirm_create_coupon_window = Window(
    Const("Создать купон❓\n"),
    Format("Купон: {dialog_data[description]}"),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_create_coupon",
        on_click=confirm_create_coupon,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToCouponsButton(),
    GoToAdminPanelButton(),
    state=CreateCouponStates.confirm,
)


create_coupon_dialog = Dialog(
    create_coupon_window,
    confirm_create_coupon_window,
)
