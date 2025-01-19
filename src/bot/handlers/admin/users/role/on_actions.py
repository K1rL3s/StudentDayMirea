from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.users.view.states import ViewUserStates
from bot.translate import translate_role
from core.enums import ALL_ROLES
from core.ids import UserId
from core.services.users import UsersService
from database.models import UserModel


async def on_role_selected(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    role = ALL_ROLES[item_id]
    dialog_manager.dialog_data["new_role"] = role
    dialog_manager.dialog_data["role_name"] = translate_role(role)
    await dialog_manager.next()


@inject
async def on_role_confirm(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    users_service: FromDishka[UsersService],
) -> None:
    role: str = dialog_manager.dialog_data["new_role"]
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    admin: UserModel = dialog_manager.middleware_data["user"]
    await users_service.change_role(user_id, admin.id, role)
    await dialog_manager.start(ViewUserStates.one, data={"view_user_id": user_id})
