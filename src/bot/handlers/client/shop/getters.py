from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import ProductId
from database.models import ProductModel, UserModel
from database.repos.products import ProductsRepo


@inject
async def get_available_products(
    products_repo: FromDishka[ProductsRepo],
    **__: Any,
) -> dict[str, list[ProductModel]]:
    products = await products_repo.get_available()
    total_stock = sum(product.stock for product in products)
    return {
        "products": products,
        "products_len": len(products),
        "total_stock": total_stock,
    }


@inject
async def get_one_product(
    dialog_manager: DialogManager,
    products_repo: FromDishka[ProductsRepo],
    **__: Any,
) -> dict[str, Any]:
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    product = await products_repo.get_by_id(product_id)
    return {"product": product}


@inject
async def get_can_buy(
    dialog_manager: DialogManager,
    products_repo: FromDishka[ProductsRepo],
    **__: Any,
) -> dict[str, Any]:
    user: UserModel = dialog_manager.middleware_data["user"]
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    product = await products_repo.get_by_id(product_id)
    return {"can_buy": user.balance >= product.price and product.stock > 0}
