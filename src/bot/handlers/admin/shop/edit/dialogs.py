from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.on_actions import on_start_update_dialog_data

from ..getters import get_one_product
from .on_actions import on_edit_price_input, on_edit_stock_input
from .states import EditProductStates

edit_price_window = Window(
    Const("🏷️ Какая новая цена?\n"),
    Format("ID: {product.id}"),
    Format("Название: {product.name}"),
    Format("Текущая цена: {product.price}"),
    MessageInput(
        func=on_edit_price_input,
        content_types=ContentType.TEXT,
        filter=F.text.cast(int) > 0,
    ),
    state=EditProductStates.price,
    getter=get_one_product,
)


edit_stock_window = Window(
    Const("📦 Какой новый запас товара?\n"),
    Format("ID: {product.id}"),
    Format("Название: {product.name}"),
    Format("Текущий запас: {product.stock}"),
    MessageInput(
        func=on_edit_stock_input,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),  # ok
    ),
    state=EditProductStates.stock,
    getter=get_one_product,
)


edit_product_dialog = Dialog(
    edit_price_window,
    edit_stock_window,
    on_start=on_start_update_dialog_data,
)
