from typing import Any

from aiogram_dialog import DialogManager

from bot.translate import translate_role
from database.models import UserModel


async def get_user_info(
    dialog_manager: DialogManager,
    **__: Any,
) -> dict[str, Any]:
    user: UserModel = dialog_manager.middleware_data["user"]
    return {
        "role": translate_role(user.role),
    }
