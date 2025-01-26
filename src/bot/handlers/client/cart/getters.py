from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from database.models import UserModel
from database.repos.purchases import PurchasesRepo


@inject
async def get_purchases(
    dialog_manager: DialogManager,
    purchases_repo: FromDishka[PurchasesRepo],
    **__: Any,
) -> dict[str, Any]:
    user: UserModel = dialog_manager.middleware_data["user"]
    purchases = await purchases_repo.get_all_user_purchases(user.id)
    purchases_info = purchases_repo.format_purchases(purchases)
    return {
        "purchases": purchases,
        "total_products": purchases_info.total_products,
        "total_purchases": purchases_info.total_purchases,
        "formated_info": purchases_info.formated_info,
        "products_to_quantity": purchases_info.product_to_quantity,
    }
