from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Multi

from bot.dialogs.buttons import GoToMenuButton

from .getters import get_purchases
from .states import CartStates

cart_window = Window(
    Multi(
        Format(
            "🧺 Куплено <u><b>{total_products}</b></u> наименований "
            "в количестве <u><b>{total_purchases}</b></u> штук",
        ),
        Format("{formated_info}"),
        Const(
            "❓ Если мероприятие закончилось, "
            "то информацию по местоположению магазинов ты найдёшь здесь —> /help",
        ),
        sep="\n\n",
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
