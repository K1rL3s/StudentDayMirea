from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format, Multi

from bot.dialogs.buttons import GoToMenuButton

from .on_actions import amount_input_handler, id_input_handler
from .states import TransferFundsStates

transfer_wait_id_window = Window(
    Const("🆔 Введи ID человека, которому хочешь перевести <b>Пятаки</b>"),
    GoToMenuButton(),
    MessageInput(
        id_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),  # ok
    ),
    state=TransferFundsStates.id,
)


transfer_wait_amount_window = Window(
    Multi(
        Format("👨‍🎓 <b>ID получателя:</b> {dialog_data[receiver_id]}"),
        Format("💳 <b>Твой баланс:</b> {middleware_data[user].balance} Пятаков"),
        Const("💸 Если всё верно, то введи сумму перевода"),
        sep="\n\n",
    ),
    GoToMenuButton(),
    MessageInput(
        amount_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text.cast(int) > 0,
    ),
    state=TransferFundsStates.amount,
)


transfer_dialog = Dialog(
    transfer_wait_id_window,
    transfer_wait_amount_window,
)
