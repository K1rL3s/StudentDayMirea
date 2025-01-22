from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Next, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToMenuButton
from bot.dialogs.filters.roles import IsSeller
from bot.dialogs.on_actions import on_start_update_dialog_data

from ..buttons import GoToProductsButton
from ..getters import get_all_products, get_one_product
from .on_actions import (
    on_confirm_delete_product,
    on_create_product,
    on_product_selected,
    on_view_qrcode,
)
from .states import ViewProductsStates

products_list_window = Window(
    Const("🛍️ Все товары"),
    ScrollingGroup(
        Select(
            Format("{item.name} | {item.price}"),
            id="products_select",
            items="products",
            on_click=on_product_selected,
            item_id_getter=lambda item: item.id,
            type_factory=int,
        ),
        width=1,
        height=10,
        hide_on_single_page=True,
        id="products_group",
    ),
    Button(
        Const("✏️ Добавить товар"),
        id="create_product",
        on_click=on_create_product,
        when=IsSeller(),
    ),
    GoToAdminPanelButton(),
    GoToMenuButton(),
    getter=get_all_products,
    state=ViewProductsStates.list,
)

view_one_product_window = Window(
    Format("ID: {product.id}"),
    Format("Название:\n{product.name}\n"),
    Format("Описание:\n{product.description}\n"),
    Format("Цена: {product.price}"),
    Format("В наличии: {product.stock}\n"),
    Button(
        Const("🖼️ Куркод товара"),
        id="qrcode",
        on_click=on_view_qrcode,
    ),
    Button(
        Const("🗑️ Удалить"),
        id="delete",
        on_click=Next(),
        when=IsSeller(),
    ),
    Back(Const("⏪ Товары")),
    GoToAdminPanelButton(),
    getter=get_one_product,
    state=ViewProductsStates.one,
)

confirm_delete_product_window = Window(
    Format("❓ Вы уверены, что хотите удалить товар ID={product.id}? "),
    Button(
        Const("✅ Подтвердить"),
        id="confirm_delete",
        on_click=on_confirm_delete_product,
    ),
    Back(Const("⏪ Отмена")),
    GoToProductsButton(),
    GoToAdminPanelButton(),
    getter=get_one_product,
    state=ViewProductsStates.confirm,
)

view_products_dialog = Dialog(
    products_list_window,
    view_one_product_window,
    confirm_delete_product_window,
    on_start=on_start_update_dialog_data,
)
