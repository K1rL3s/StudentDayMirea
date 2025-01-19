from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Column, Select
from aiogram_dialog.widgets.text import Const, Format, Multi

from bot.dialogs.buttons import GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import get_all_known_quests, get_quest_by_id
from .on_actions import on_answer, on_quest_selected
from .states import ViewQuestsStates

view_quests_window = Window(
    Const("Найденные квестовые записки"),
    Column(
        Select(
            Multi(
                Const("✅ ", when=F["item"][1].status),
                Format("{item[0].title}"),
                sep="",
            ),
            id="quests_select",
            item_id_getter=lambda item: item[0].id,
            items="quests",
            type_factory=str,
            on_click=on_quest_selected,
        ),
    ),
    GoToMenuButton(),
    getter=get_all_known_quests,
    state=ViewQuestsStates.list,
)

view_quest_window = Window(
    Multi(
        Const("✅ ", when=F["status"]),
        Format("{quest.title}\n\n"),
        Format("{quest.description}\n\n"),
        Format("{quest.task}"),
        sep="",
    ),
    Button(
        Const("✏️ Ввести ответ"),
        id="answer",
        on_click=on_answer,
        when=~F["status"],
    ),
    Back(Const("⏪ Все записки")),
    GoToMenuButton(),
    getter=get_quest_by_id,
    state=ViewQuestsStates.one,
)

view_quests_dialog = Dialog(
    view_quests_window,
    view_quest_window,
    on_start=on_start_update_dialog_data,
)
