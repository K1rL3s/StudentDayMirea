from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import UserId
from database.repos.coupons import CouponsRepo


@inject
async def get_coupon(
    dialog_manager: DialogManager,
    coupons_repo: FromDishka[CouponsRepo],
    **__: Any,
) -> dict[str, Any]:
    user_id: UserId = dialog_manager.middleware_data["user_id"]
    coupon = await coupons_repo.get_by_user_id(user_id)
    return {"coupon": coupon}
