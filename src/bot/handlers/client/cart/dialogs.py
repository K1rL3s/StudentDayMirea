from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton

from .getters import get_purchases
from .states import CartStates

cart_window = Window(
    Format(
        "🧺 Куплено {total_products} наименований в количестве {total_purchases} штук\n"
        "Чтобы их забрать, подойди к <u>магазину</u> или в <u>Отделение А-337</u>\n\n"
        "{formated_info}",
        when=F["total_purchases"],
    ),
    Const(
        "🧺 Корзина пустая",
        when=~F["total_purchases"],
    ),
    GoToMenuButton(),
    getter=get_purchases,
    state=CartStates.cart,
)


cart_dialog = Dialog(cart_window)
