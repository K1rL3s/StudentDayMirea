from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton

from .on_actions import amount_input_handler, id_input_handler
from .states import TransferFundsStates

transfer_wait_id_window = Window(
    Const("Введите ID человека, которому хотите перевести <b>Пятаки</b>"),
    GoToMenuButton(),
    MessageInput(
        id_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    state=TransferFundsStates.id,
)


transfer_wait_amount_window = Window(
    Format(
        "Имя получателя: <b>{dialog_data[receiver_name]}</b>\n\n"
        "Если всё верно, то введите сумму перевода\n"
        "Ваш баланс: {middleware_data[user].balance} Пятаков",
    ),
    GoToMenuButton(),
    MessageInput(
        amount_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    state=TransferFundsStates.amount,
)


transfer_dialog = Dialog(
    transfer_wait_id_window,
    transfer_wait_amount_window,
)
