from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton
from bot.dialogs.filters.roles import IsAdmin, IsLottery, IsStager, IsWithRole

from .getters import get_user_info, get_users_count
from .on_actions import (
    on_go_to_broadcast,
    on_go_to_coupons,
    on_go_to_lottery,
    on_go_to_quest,
    on_go_to_secrets,
    on_go_to_shop,
    on_go_to_tasks,
    on_go_to_view_users,
)
from .states import AdminPanelStates

admin_panel_window = Window(
    Format("❗Админ-панель, ты - <u>{role}</u>\n"),
    Format(
        "👨🏻‍🎓 Зарегистрировано <b>{all_users}</b> и активно <b>{active_users}</b>",
        when=IsAdmin(),
    ),
    Group(
        Button(
            Const("📢 Рассылка"),
            id="broadcast",
            on_click=on_go_to_broadcast,
            when=IsAdmin(),
        ),
        Button(
            Const("👥 Пользователи"),
            id="users",
            on_click=on_go_to_view_users,
            when=IsWithRole(),
        ),
        Button(
            Const("🛍️ Товары"),
            id="products",
            on_click=on_go_to_shop,
            when=IsAdmin(),
        ),
        Button(
            Const("🤫 Секреты"),
            id="secrets",
            on_click=on_go_to_secrets,
            when=IsAdmin(),
        ),
        Button(
            Const("🧠 Задания"),
            id="tasks",
            on_click=on_go_to_tasks,
            when=IsStager(),
        ),
        Button(
            Const("🗺️ Квест"),
            id="quest",
            on_click=on_go_to_quest,
            when=IsStager(),
        ),
        Button(
            Const("🎟️ Лотерея"),
            id="lottery",
            on_click=on_go_to_lottery,
            when=IsLottery(),
        ),
        Button(
            Const("🛴 Купоны"),
            id="coupons",
            on_click=on_go_to_coupons,
            when=IsAdmin(),
        ),
        width=2,
    ),
    GoToMenuButton(),
    getter=[get_user_info, get_users_count],
    state=AdminPanelStates.panel,
)

admin_panel_dialog = Dialog(admin_panel_window)
