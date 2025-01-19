from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart, MagicData, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.filters.roles import IsSeller
from core.services.products import ProductsService
from core.services.qrcodes import ProductIdPrefix
from database.repos.products import ProductsRepo

from .view.states import ViewProductsStates

router = Router(name=__file__)


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith(ProductIdPrefix)),
    MagicData(F.command.args.as_("product_deeplink")),
    IsSeller(),
)
async def open_product_by_deeplink(
    message: Message,
    product_deeplink: str,
    dialog_manager: DialogManager,
    products_repo: FromDishka[ProductsRepo],
) -> None:
    product_id = product_deeplink.lstrip(ProductIdPrefix)
    if product_id.isdigit():
        product_id = int(product_id)
        if await products_repo.get_by_id(product_id):
            await dialog_manager.start(
                ViewProductsStates.one,
                data={"product_id": product_id},
            )


@router.message(Command("stock"), StateFilter(None))
async def admin_update_stock(
    message: Message,
    command: CommandObject,
    products_service: FromDishka[ProductsService],
) -> None:
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        product_id, new_stock = int(args[0]), int(args[1])
        await products_service.set_stock(product_id, new_stock)
        await message.answer(
            f"Количество товара с ID {product_id} обновлено до {new_stock}",
        )
    else:
        await message.answer("Формат: /stock <id> <new_stock>", parse_mode=None)


@router.message(Command("price"), StateFilter(None))
async def admin_change_product_price(
    message: Message,
    command: CommandObject,
    products_service: FromDishka[ProductsService],
) -> None:
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        product_id, new_price = int(args[0]), int(args[1])
        await products_service.set_price(product_id, new_price)
        await message.answer(
            f"Цена товара с ID {product_id} изменена на {new_price}",
        )
    else:
        await message.answer("Формат: /price <id> <new_price>", parse_mode=None)
