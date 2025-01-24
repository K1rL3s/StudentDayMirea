from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Column, Next, Row, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToQuestsButton
from ..getters import get_all_quests, get_quest_by_id
from .on_actions import (
    on_confirm_delete_quest,
    on_create_quest,
    on_edit_reward,
    on_quest_selected,
    on_view_qrcode,
)
from .states import AdminViewQuestsStates

quests_list_window = Window(
    Const("🗺️ Все квестовые задания"),
    Column(
        Select(
            Format("{item.order} | {item.id} | {item.title}"),
            id="quests_select",
            items="quests",
            on_click=on_quest_selected,
            item_id_getter=lambda item: item.id,
            type_factory=str,
        ),
    ),
    Button(Const("✏️ Создать задание"), id="create_quest", on_click=on_create_quest),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_all_quests,
    state=AdminViewQuestsStates.list,
)

view_one_quest_window = Window(
    Format("ID: {quest.id}"),
    Format("Название:\n{quest.title}\n"),
    Format("Награда: {quest.reward}"),
    Format("Описание:\n{quest.description}\n"),
    Format("Задание:\n{quest.task}\n"),
    Format("Ответ:\n{quest.answer}\n"),
    Format("Подсказка после ответа:\n{quest.end_hint}\n"),
    Button(Const("🖼️ Куркод задания"), id="qrcode", on_click=on_view_qrcode),
    Row(
        Button(
            Const("💰 Изменить награду"),
            id="reward",
            on_click=on_edit_reward,
        ),
    ),
    Button(Const("🗑️ Удалить"), id="delete", on_click=Next()),
    Back(Const("⏪ Задания")),
    GoToAdminPanelButton(),
    getter=get_quest_by_id,
    state=AdminViewQuestsStates.one,
)

confirm_delete_quest_window = Window(
    Format("❓ Вы уверены, что хотите удалить задание ID={quest.id}? "),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_delete",
        on_click=on_confirm_delete_quest,
    ),
    Back(Const("⏪ Отмена")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    getter=get_quest_by_id,
    state=AdminViewQuestsStates.confirm,
)

view_quests_dialog = Dialog(
    quests_list_window,
    view_one_quest_window,
    confirm_delete_quest_window,
    on_start=on_start_update_dialog_data,
)
