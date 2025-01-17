from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton

from .on_actions import user_id_input_handler
from .states import LotteryStartInputStates

user_id_window = Window(
    Const("Введите айди пользователя в боте"),
    MessageInput(
        user_id_input_handler,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    state=LotteryStartInputStates.user_id,
)

lottery_user_id_dialog = Dialog(user_id_window)
