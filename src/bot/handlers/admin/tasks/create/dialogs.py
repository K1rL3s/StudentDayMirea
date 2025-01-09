from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToTasksButton
from .on_actions import (
    confirm_create_task,
    task_description_input,
    task_end_phrase_input,
    task_reward_input,
    task_title_input,
)
from .states import CreateTaskStates

task_title_window = Window(
    Const("Введите название (заголовок) задания (256 символов)"),
    MessageInput(
        func=task_title_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    GoToTasksButton(),
    state=CreateTaskStates.title,
)

task_description_window = Window(
    Const("Введите описание задания (2048 символов)"),
    MessageInput(
        func=task_description_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToTasksButton(),
    GoToAdminPanelButton(),
    state=CreateTaskStates.description,
)

task_reward_window = Window(
    Const("Какая награда за задание? Число больше нуля"),
    MessageInput(
        func=task_reward_input,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    Back(Const("⏪ Шаг назад")),
    GoToTasksButton(),
    GoToAdminPanelButton(),
    state=CreateTaskStates.reward,
)

task_end_phrase_window = Window(
    Const("Введите фразу для завершения задания (256 символов)"),
    MessageInput(
        func=task_end_phrase_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToTasksButton(),
    GoToAdminPanelButton(),
    state=CreateTaskStates.end_phrase,
)


confirm_create_task_window = Window(
    Const("❓ Создать задание?"),
    Format("Название: {dialog_data[title]}"),
    Format("Награда: {dialog_data[reward]}\n"),
    Format("Описание:\n{dialog_data[description]}\n"),
    Format("Завершающая фраза:\n{dialog_data[end_phrase]}"),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_create",
        on_click=confirm_create_task,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToTasksButton(),
    GoToAdminPanelButton(),
    state=CreateTaskStates.confirm,
)


create_task_dialog = Dialog(
    task_title_window,
    task_description_window,
    task_reward_window,
    task_end_phrase_window,
    confirm_create_task_window,
    on_start=on_start_update_dialog_data,
)
