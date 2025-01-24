from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.on_actions import on_start_update_dialog_data

from .on_actions import name_handler, register_confirm, register_disconfirm
from .states import StartStates

START_TEXT = """
<b>Здарова! 👋 </b>

<b>Я — Кузя</b>, и я помогу тебе разобраться во всём, чем можно заняться на Дне студента!

💰 Я главный по <b>Пятакам</b>, буду следить, сколько у тебя их накопилось, и напоминать про самые интересные события ко Дню студента.

Для регистрации просто введи свою <b>фамилию и имя</b>.
<i>(Пример: Иванов Ваня)</i>
""".strip()  # noqa

BAD_FORMAT = "Неверный формат!"

REGISTER_TEXT = """
Для регистрации просто введи свою <b>фамилию и имя</b>.
<i>(Пример: Иванов Ваня)</i>
""".strip()


welcome_window = Window(
    Const(
        START_TEXT,
        when=~F["dialog_data"]["retry"],
    ),
    Const(BAD_FORMAT, when=F["dialog_data"]["retry"]),
    Const("\n" + REGISTER_TEXT),
    MessageInput(name_handler, content_types=[ContentType.TEXT]),
    state=StartStates.name,
)
confirm_name_window = Window(
    Const("❗ Проверь введённые данные!\n"),
    Format("Тебя зовут <b>{dialog_data[full_name]}</b>?"),
    Button(Const("✅ Подтвердить"), id="yes", on_click=register_confirm),
    Button(Const("🔁 Повторить ввод"), id="no", on_click=register_disconfirm),
    state=StartStates.confirm,
)

start_dialog = Dialog(
    welcome_window,
    confirm_name_window,
    on_start=on_start_update_dialog_data,
)
