from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import Widget
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import ProductId
from core.services.products import ProductsService
from database.models import UserModel
from database.repos.products import ProductsRepo


async def on_product_selected(
    _: CallbackQuery,
    __: Widget,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    dialog_manager.dialog_data["product_id"] = item_id
    await dialog_manager.next()


@inject
async def on_buy_product(
    _: CallbackQuery,
    __: Widget,
    dialog_manager: DialogManager,
    products_repo: FromDishka[ProductsRepo],
    products_service: FromDishka[ProductsService],
) -> None:
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    user: UserModel = dialog_manager.middleware_data["user"]
    product = await products_repo.get_by_id(product_id)

    if product.stock <= 0:
        dialog_manager.dialog_data["final_message"] = "Упс, продукт уже раскупили"
    elif user.balance < product.price:
        dialog_manager.dialog_data["final_message"] = (
            "Упс, у тебя недостаточно <b>Пятаков</b>!"
        )
    else:
        await products_service.buy_product(user.id, product.id, 1)
        dialog_manager.dialog_data["final_message"] = (
            "Товар оплачен и добавлен в корзину!"
        )

    await dialog_manager.next()
