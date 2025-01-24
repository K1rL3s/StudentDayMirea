from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import get_quest_by_id
from .on_actions import on_edit_reward_input
from .states import EditQuestStates

edit_phrase_window = Window(
    Const("💰 Какая новая награда?\n"),
    Format("ID: {quest.id}"),
    Format("Текущая награда: {quest.reward}"),
    MessageInput(
        func=on_edit_reward_input,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    state=EditQuestStates.reward,
    getter=get_quest_by_id,
)


edit_quest_dialog = Dialog(
    edit_phrase_window,
    on_start=on_start_update_dialog_data,
)
