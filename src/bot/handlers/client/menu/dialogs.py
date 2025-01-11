from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToTaskButton
from bot.dialogs.filters.roles import IsWithRole

from .getters import get_user_info
from .on_actions import on_cart, on_help, on_lottery, on_shop, on_transfer_funds
from .states import MenuStates

menu_dialog = Dialog(
    Window(
        Const("<b>Главное меню</b>\n"),
        Format("Ваш ID: <code>{user_id}</code> (/id)"),
        Format("Баланс: {balance} <b>Пятаков</b>\n"),
        Format("Вы - <u>{role}</u>", when=IsWithRole()),
        Group(
            Button(Const("🛍️ Магазин"), id="shop", on_click=on_shop),
            Button(Const("🧺 Корзина"), id="cart", on_click=on_cart),
            Button(Const("💸 Перевод"), id="transfer", on_click=on_transfer_funds),
            GoToTaskButton(),
            Button(Const("🎟️ Лотерея"), id="lottery", on_click=on_lottery),
            Button(Const("🆘 Помощь"), id="help", on_click=on_help),
            width=2,
        ),
        GoToAdminPanelButton(when=IsWithRole()),
        getter=get_user_info,
        state=MenuStates.menu,
    ),
)
