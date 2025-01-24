from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Next
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToQuestsButton
from .on_actions import (
    confirm_create_quest,
    quest_answer_input,
    quest_description_input,
    quest_end_hint_input,
    quest_image_input,
    quest_order_input,
    quest_reward_input,
    quest_right_answer_input,
    quest_task_input,
    quest_title_input,
    quest_wrong_answer_input,
)
from .states import CreateQuestStates

order_window = Window(
    Const("1️⃣ Введи порядковый номер задания"),
    MessageInput(
        func=quest_order_input,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.order,
)

title_window = Window(
    Const("2️⃣ Введи название (заголовок) задания (64 символов)"),
    MessageInput(
        func=quest_title_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.title,
)

description_window = Window(
    Const("3️⃣ Введи описание задания (2048 символов)"),
    MessageInput(
        func=quest_description_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.description,
)

task_window = Window(
    Const("4️⃣ Введи задание задания (1024 символов)"),
    MessageInput(
        func=quest_task_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.task,
)

image_window = Window(
    Const("5️⃣ Отправь картинку для задания"),
    MessageInput(
        func=quest_image_input,
        content_types=ContentType.PHOTO,
    ),
    Next(Const("⏩ Без изображения")),
    Back(Const("⏪ Шаг назад")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.image,
)

reward_window = Window(
    Const("6️⃣ Какая награда за задание? Число больше нуля"),
    MessageInput(
        func=quest_reward_input,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    Back(Const("⏪ Шаг назад")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.reward,
)

answer_window = Window(
    Const("7️⃣ Введи ответ на задание (128 символов)"),
    MessageInput(
        func=quest_answer_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.answer,
)

end_hint_window = Window(
    Const("8️⃣ Введи подсказку на следующий квест (256 символов)"),
    MessageInput(
        func=quest_end_hint_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.end_hint,
)

right_answer_window = Window(
    Const("9️ Введи текст на верный ответ (128 символов)"),
    MessageInput(
        func=quest_right_answer_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.right_answer,
)


wrong_answer_window = Window(
    Const("1️⃣0️⃣ Введи текст на неверный ответ (128 символов)"),
    MessageInput(
        func=quest_wrong_answer_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.wrong_answer,
)


confirm_create_quest_window = Window(
    Const("Создать задание❓\n"),
    Format("Порядковый номер: {dialog_data[order]}"),
    Format("Название:\n{dialog_data[title]}\n"),
    Format("Описание:\n{dialog_data[description]}\n"),
    Format("Задание:\n{dialog_data[task]}\n"),
    Format("Изображение: {dialog_data[image_id]}", when=F["dialog_data"]["image_id"]),
    Format("Награда: {dialog_data[reward]}"),
    Format("Ответ:\n{dialog_data[answer]}\n"),
    Format("Подсказка после ответа:\n{dialog_data[end_hint]}\n"),
    Format("На правильный ответ:\n{dialog_data[right_answer]}\n"),
    Format("На неверный ответа:\n{dialog_data[wrong_answer]}\n"),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_create",
        on_click=confirm_create_quest,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToQuestsButton(),
    GoToAdminPanelButton(),
    state=CreateQuestStates.confirm,
)


create_quest_dialog = Dialog(
    order_window,
    title_window,
    description_window,
    task_window,
    image_window,
    reward_window,
    answer_window,
    end_hint_window,
    right_answer_window,
    wrong_answer_window,
    confirm_create_quest_window,
    on_start=on_start_update_dialog_data,
)
