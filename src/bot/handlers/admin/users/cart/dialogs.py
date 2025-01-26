from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Multiselect,
    Next,
    Row,
    ScrollingGroup,
)
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToUserButton
from ..getters import get_view_user_info
from ..on_actions import UserAdminInfoText
from .getters import get_view_user_cart
from .on_actions import on_cart_item_selected, on_clear_cart_confirm
from .states import CartUserStates

user_cart_window = Window(
    UserAdminInfoText,
    Format(
        "Куплено {total_products} наименований в количестве {total_purchases} штук",
        when=F["total_purchases"],
    ),
    Format("Корзина пустая", when=~F["total_purchases"]),
    Format("\n{formated_info}"),
    ScrollingGroup(
        Multiselect(
            checked_text=Format("🔘 {item[0][1]}: {item[1]}"),
            unchecked_text=Format("{item[0][1]}: {item[1]}"),
            id="select",
            item_id_getter=lambda p: p[0][0],
            items="products_to_quantity",
            type_factory=int,
            on_state_changed=on_cart_item_selected,
        ),
        height=10,
        width=1,
        hide_on_single_page=True,
        id="cart_pager",
    ),
    Button(
        Const("🗑️ Очистить корзину"),
        id="clear",
        on_click=Next(),
        when=F["dialog_data"]["selected"],
    ),
    GoToUserButton,
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=[get_view_user_info, get_view_user_cart],
    state=CartUserStates.cart,
)

clear_cart_window = Window(
    Format(
        "❓ Уверен, что хочешь очистить выделенные позиции из корзины "
        "пользователю {view_user.id} - {view_user.name}?",
    ),
    Row(
        Back(Const("⏪ Корзина")),
        Button(Const("✅ Подтвердить"), id="confirm", on_click=on_clear_cart_confirm),
    ),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_view_user_info,
    state=CartUserStates.clear,
)

user_cart_dialog = Dialog(
    user_cart_window,
    clear_cart_window,
    on_start=on_start_update_dialog_data,
)
