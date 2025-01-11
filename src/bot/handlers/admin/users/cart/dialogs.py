from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Next, Row
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import user_short_link
from ..on_actions import _UserIdNameText, on_go_view_user
from .getters import get_view_user_cart
from .on_actions import on_clear_cart_confirm
from .states import CartUserStates

user_cart_window = Window(
    _UserIdNameText,
    Format("Куплено {total_products} наименований в количестве {total_purchases} штук"),
    Format("\n{formated_info}"),
    Button(Const("🗑️ Очистить корзину"), id="clear_cart", on_click=Next()),
    Button(Const("⏪ Юзер"), id="back", on_click=on_go_view_user),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=[user_short_link, get_view_user_cart],
    state=CartUserStates.cart,
)

clear_cart_window = Window(
    Format(
        "Уверены, что хотите очистить корзину "
        "пользователю {view_user.id} - {view_user.name}?",
    ),
    Row(
        Back(Const("⏪ Корзина")),
        Button(Const("✅ Подтвердить"), id="confirm", on_click=on_clear_cart_confirm),
    ),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=user_short_link,
    state=CartUserStates.clear,
)


user_cart_dialog = Dialog(
    user_cart_window,
    clear_cart_window,
    on_start=on_start_update_dialog_data,
)
