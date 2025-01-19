from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.shop.view.states import ViewProductsStates
from core.ids import UserId
from core.services.products import ProductsService


async def product_name_input(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    name = message.html_text.strip()[:64]
    dialog_manager.dialog_data["name"] = name
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def product_description_input(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    description = message.html_text.strip()[:2048]
    dialog_manager.dialog_data["description"] = description
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def product_price_input(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    price = int(message.text)
    dialog_manager.dialog_data["price"] = price
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def product_stock_input(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    stock = int(message.text)
    dialog_manager.dialog_data["stock"] = stock
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


@inject
async def confirm_create_product(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    products_service: FromDishka[ProductsService],
) -> None:
    name: str = dialog_manager.dialog_data["name"]
    description: str = dialog_manager.dialog_data["description"]
    price: int = dialog_manager.dialog_data["price"]
    stock: int = dialog_manager.dialog_data["stock"]
    user_id: UserId = dialog_manager.middleware_data["user_id"]

    product_id = await products_service.create(name, description, price, stock, user_id)

    await dialog_manager.start(
        state=ViewProductsStates.one,
        data={"product_id": product_id},
    )
