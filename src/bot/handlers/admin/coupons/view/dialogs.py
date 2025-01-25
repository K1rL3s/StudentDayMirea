from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToCouponsButton
from ..getters import get_all_coupons, get_one_coupon
from .on_actions import (
    on_confirm_delete_coupon,
    on_coupon_selected,
    on_create_coupon,
    on_delete_coupon,
)
from .states import ViewCouponsStates

coupons_list_window = Window(
    Const("🛴 Все купоны\n"),
    Format("📈 Всего {total} купонов, активировано {activated} "),
    ScrollingGroup(
        Select(
            Format("{item.id} | {item.description}"),
            id="coupons_select",
            items="coupons",
            on_click=on_coupon_selected,
            item_id_getter=lambda item: item.id,
            type_factory=int,
        ),
        width=1,
        height=10,
        hide_on_single_page=True,
        id="coupons_group",
    ),
    Button(
        Const("✏️ Создать купон"),
        id="create",
        on_click=on_create_coupon,
    ),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_all_coupons,
    state=ViewCouponsStates.list,
)

view_one_coupon_window = Window(
    Format("ID: {coupon.id}"),
    Format("Купон: {coupon.description}\n"),
    Format(
        "Активирован юзером: {coupon_user.id} {coupon_user.name}",
        when=F["coupon_user"],
    ),
    Button(
        Const("🗑️ Удалить"),
        id="delete",
        on_click=on_delete_coupon,
    ),
    Back(Const("⏪ Cекреты")),
    GoToAdminPanelButton(),
    getter=get_one_coupon,
    state=ViewCouponsStates.one,
)

confirm_delete_coupon_window = Window(
    Format("Ты уверен, что хочешь удалить купон ID={coupon.id}❓"),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_delete",
        on_click=on_confirm_delete_coupon,
    ),
    Back(Const("⏪ Отмена")),
    GoToCouponsButton(),
    GoToAdminPanelButton(),
    getter=get_one_coupon,
    state=ViewCouponsStates.confirm,
)

view_coupons_dialog = Dialog(
    coupons_list_window,
    view_one_coupon_window,
    confirm_delete_coupon_window,
    on_start=on_start_update_dialog_data,
)
