from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Next, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToTasksButton
from ..getters import get_all_tasks, get_task_by_id
from .on_actions import (
    on_confirm_delete_task,
    on_create_task,
    on_task_selected,
    on_view_qrcode,
)
from .states import ViewTasksStates

tasks_list_window = Window(
    Const("🧠 Все задания"),
    ScrollingGroup(
        Select(
            Format("{item.id} | {item.title}"),
            id="tasks_select",
            items="tasks",
            on_click=on_task_selected,
            item_id_getter=lambda item: item.id,
            type_factory=str,
        ),
        width=1,
        height=10,
        hide_on_single_page=True,
        id="tasks_group",
    ),
    Button(Const("✏️ Создать задание"), id="create_task", on_click=on_create_task),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_all_tasks,
    state=ViewTasksStates.list,
)

view_one_task_window = Window(
    Format("ID: {task.id}"),
    Format("Название:\n{task.title}\n"),
    Format("Описание:\n{task.description}\n"),
    Format("Ответ:\n{task.answer}\n"),
    Button(Const("🖼️ Куркод задания"), id="qrcode", on_click=on_view_qrcode),
    Button(
        Const("🗑️ Удалить"),
        id="delete",
        on_click=Next(),
    ),
    Back(Const("⏪ Задания")),
    GoToAdminPanelButton(),
    getter=get_task_by_id,
    state=ViewTasksStates.one,
)

confirm_delete_task_window = Window(
    Format("❓ Вы уверены, что хотите удалить задание ID={task.id}? "),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_delete",
        on_click=on_confirm_delete_task,
    ),
    Back(Const("⏪ Отмена")),
    GoToTasksButton(),
    GoToAdminPanelButton(),
    getter=get_task_by_id,
    state=ViewTasksStates.confirm,
)

view_tasks_dialog = Dialog(
    tasks_list_window,
    view_one_task_window,
    confirm_delete_task_window,
    on_start=on_start_update_dialog_data,
)
