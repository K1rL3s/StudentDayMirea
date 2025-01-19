from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToProductsButton
from .on_actions import (
    confirm_create_product,
    product_description_input,
    product_name_input,
    product_price_input,
    product_stock_input,
)
from .states import CreateProductStates

product_name_window = Window(
    Const("1️⃣ Введите название товара (64 символа)"),
    MessageInput(
        func=product_name_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    GoToProductsButton(),
    state=CreateProductStates.name,
)

product_description_window = Window(
    Const("2️⃣ Введите описание товара (2048 символов)"),
    MessageInput(
        func=product_description_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToProductsButton(),
    GoToAdminPanelButton(),
    state=CreateProductStates.description,
)

product_price_window = Window(
    Const("3️⃣ Цена товара? Число больше нуля"),
    MessageInput(
        func=product_price_input,
        content_types=ContentType.TEXT,
        filter=F.text.isdigit(),
    ),
    Back(Const("⏪ Шаг назад")),
    GoToProductsButton(),
    GoToAdminPanelButton(),
    state=CreateProductStates.price,
)

product_stock_window = Window(
    Const("4️⃣ Сколько доступно товара (в наличии)? Число больше нуля"),
    MessageInput(
        func=product_stock_input,
        content_types=ContentType.TEXT,
        filter=F.text,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToProductsButton(),
    GoToAdminPanelButton(),
    state=CreateProductStates.stock,
)


confirm_create_product_window = Window(
    Const("Создать товар❓\n"),
    Format("Название: {dialog_data[name]}"),
    Format("Цена: {dialog_data[price]}"),
    Format("В наличии: {dialog_data[stock]}"),
    Format("Описание:\n{dialog_data[description]}"),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_create",
        on_click=confirm_create_product,
    ),
    Back(Const("⏪ Шаг назад")),
    GoToProductsButton(),
    GoToAdminPanelButton(),
    state=CreateProductStates.confirm,
)


create_product_dialog = Dialog(
    product_name_window,
    product_description_window,
    product_price_window,
    product_stock_window,
    confirm_create_product_window,
    on_start=on_start_update_dialog_data,
)
