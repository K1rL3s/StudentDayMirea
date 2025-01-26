from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import get_one_secret
from .on_actions import (
    on_edit_activation_limit_input,
    on_edit_phrase_input,
    on_edit_reward_input,
)
from .states import EditSecretStates

edit_phrase_window = Window(
    Const("💬 Какая новая фраза секрета?\n"),
    Format("ID: {secret.id}"),
    Format("Текущая фраза: {secret.phrase}"),
    MessageInput(
        func=on_edit_phrase_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    state=EditSecretStates.phrase,
    getter=get_one_secret,
)

edit_reward_window = Window(
    Const("💰 Какая новая награда?\n"),
    Format("ID: {secret.id}"),
    Format("Фраза: {secret.phrase}"),
    Format("Текущая цена: {secret.reward}"),
    MessageInput(
        func=on_edit_reward_input,
        content_types=ContentType.TEXT,
        filter=F.text.cast(int) > 0,
    ),
    state=EditSecretStates.reward,
    getter=get_one_secret,
)

edit_activation_limit_window = Window(
    Const("🚀 Какой новый лимит активаций?\n"),
    Format("ID: {secret.id}"),
    Format("Фраза: {secret.phrase}"),
    Format("Всего активировано: {total_activations}"),
    Format("Текущий лимит: {secret.activation_limit}"),
    MessageInput(
        func=on_edit_activation_limit_input,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),  # ok
    ),
    state=EditSecretStates.activation_limit,
    getter=get_one_secret,
)

edit_secret_dialog = Dialog(
    edit_phrase_window,
    edit_reward_window,
    edit_activation_limit_window,
    on_start=on_start_update_dialog_data,
)
