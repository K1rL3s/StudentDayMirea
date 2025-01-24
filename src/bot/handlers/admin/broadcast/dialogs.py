from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton

from .on_actions import on_input_broadcast_message, start_broadcast
from .states import BroadcastStates

wait_message_window = Window(
    Const("ℹ️ Введи сообщение для рассылки"),
    GoToAdminPanelButton("⏪ Админ-панель"),
    MessageInput(
        func=on_input_broadcast_message,
        content_types=[ContentType.TEXT, ContentType.PHOTO],
    ),
    state=BroadcastStates.wait,
)


confirm_window = Window(
    Const("👀 Сообщение в рассылке будет выглядеть так:\n"),
    Format("{dialog_data[broadcast_message]}"),
    Button(Const("✅ Подтвердить"), id="confirm", on_click=start_broadcast),
    Back(Const("🔁 Ввести заново")),
    GoToAdminPanelButton(),
    state=BroadcastStates.confirm,
)


broadcast_dialog = Dialog(
    wait_message_window,
    confirm_window,
)
