from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton

from ..buttons import GoToSecretsButton
from .on_actions import (
    confirm_create_secret,
    secret_activation_limit_input,
    secret_phrase_input,
    secret_reward_input,
)
from .states import CreateSecretStates

create_secret_window = Window(
    Const("1️⃣ Введите секретную фразу"),
    MessageInput(
        func=secret_phrase_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    GoToSecretsButton(),
    state=CreateSecretStates.phrase,
)

secret_reward_window = Window(
    Const("2️⃣ Какая награда? Число больше нуля"),
    MessageInput(
        func=secret_reward_input,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    Back(Const("⏪ Шаг назад")),
    GoToSecretsButton(),
    GoToAdminPanelButton(),
    state=CreateSecretStates.reward,
)

secret_activation_limit_window = Window(
    Const("3️⃣ Сколько активаций? Число больше нуля"),
    MessageInput(
        func=secret_activation_limit_input,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    Back(Const("⏪ Шаг назад")),
    GoToSecretsButton(),
    GoToAdminPanelButton(),
    state=CreateSecretStates.activation_limit,
)

confirm_create_secret_window = Window(
    Const("❓ Создать секрет?"),
    Format("Фраза: <code>{dialog_data[phrase]}</code>"),
    Format("Награда: {dialog_data[reward]}"),
    Format("Активаций: {dialog_data[activation_limit]}"),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_create_secret",
        on_click=confirm_create_secret,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToSecretsButton(),
    GoToAdminPanelButton(),
    state=CreateSecretStates.confirm,
)


create_secret_dialog = Dialog(
    create_secret_window,
    secret_reward_window,
    secret_activation_limit_window,
    confirm_create_secret_window,
)
