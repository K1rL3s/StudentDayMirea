from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToQuestButton, GoToQuestsButton
from ..getters import get_quest_by_id
from .on_actions import (
    on_edit_image_input,
    on_edit_reward_input,
    on_edit_without_image_input,
)
from .states import EditQuestStates

edit_reward_window = Window(
    Const("💰 Какая новая награда?\n"),
    Format("ID: {quest.id}"),
    Format("Текущая награда: {quest.reward}"),
    MessageInput(
        func=on_edit_reward_input,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    GoToQuestButton(),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=EditQuestStates.reward,
    getter=get_quest_by_id,
)

edit_image_window = Window(
    Const("🖼️ Какое новое изображение\n"),
    Format("ID: {quest.id}"),
    MessageInput(
        func=on_edit_image_input,
        content_types=ContentType.PHOTO,
        filter=F.photo,
    ),
    Button(
        Const("🗑️ Удалить изображение"),
        id="clear",
        on_click=on_edit_without_image_input,
        when=F["quest"].image_id,
    ),
    GoToQuestButton(),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=EditQuestStates.image,
    getter=get_quest_by_id,
)


edit_quest_dialog = Dialog(
    edit_reward_window,
    edit_image_window,
    on_start=on_start_update_dialog_data,
)
