from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import CouponId
from database.repos.coupons import CouponsRepo


@inject
async def get_all_coupons(
    coupons_repo: FromDishka[CouponsRepo],
    **__: Any,
) -> dict[str, Any]:
    coupons = await coupons_repo.get_all()
    return {"coupons": coupons}


@inject
async def get_one_coupon(
    dialog_manager: DialogManager,
    coupons_repo: FromDishka[CouponsRepo],
    **__: Any,
) -> dict[str, Any]:
    coupon_id: CouponId = dialog_manager.dialog_data["coupon_id"]
    coupon, coupon_user = await coupons_repo.get_by_id(coupon_id)
    return {"coupon": coupon, "coupon_user": coupon_user}
