from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import ProductId, TgId
from core.services.products import ProductsService
from core.services.qrcode_saver import QRCodeSaver
from database.models import UserModel
from database.repos.products import ProductsRepo

from ..create.states import CreateProductStates
from ..edit.states import EditProductStates
from .states import ViewProductsStates


async def on_product_selected(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    dialog_manager.dialog_data["product_id"] = item_id
    await dialog_manager.next()


async def on_create_product(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=CreateProductStates.name)


async def on_edit_price(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    await dialog_manager.start(
        state=EditProductStates.price,
        data={"product_id": product_id},
    )


async def on_edit_stock(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    await dialog_manager.start(
        state=EditProductStates.stock,
        data={"product_id": product_id},
    )


@inject
async def on_view_qrcode(
    callback: CallbackQuery,
    _: Button,
    dialog_manager: DialogManager,
    products_repo: FromDishka[ProductsRepo],
    qrcode_saver: FromDishka[QRCodeSaver],
) -> None:
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    text = f"Товар, ID: <code>{product_id}</code>"
    product = await products_repo.get_by_id(product_id)

    if product.qrcode_image_id:
        await callback.message.answer_photo(photo=product.qrcode_image_id, caption=text)
    else:
        await qrcode_saver.product(text, product.id, TgId(callback.from_user.id))

    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND


@inject
async def on_confirm_delete_product(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    products_service: FromDishka[ProductsService],
) -> None:
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    master: UserModel = dialog_manager.middleware_data["user"]
    await products_service.delete(product_id, master.id)
    await dialog_manager.start(state=ViewProductsStates.list)
