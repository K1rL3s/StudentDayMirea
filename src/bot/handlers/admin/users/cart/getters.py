from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import UserId
from database.repos.purchases import PurchasesRepo
from database.repos.users import UsersRepo


@inject
async def get_view_user_cart(
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
    purchases_repo: FromDishka[PurchasesRepo],
    **__: Any,
) -> dict[str, Any]:
    user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    user = await users_repo.get_by_id(user_id)
    purchases = await purchases_repo.get_user_purchases(user.id)
    purchases_info = purchases_repo.format_purchases(purchases)
    return {
        "total_products": purchases_info.total_products,
        "total_purchases": purchases_info.total_purchases,
        "formated_info": purchases_info.formated_info,
        "purchases": purchases,
        "products_to_quantity": purchases_info.product_to_quantity,
    }
