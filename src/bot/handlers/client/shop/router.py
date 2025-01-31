from aiogram import F, Router
from aiogram.filters import Command, CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.enums import SlashCommand
from bot.handlers.client.shop.states import ShopStates
from core.ids import ProductId
from core.services.qrcodes import ProductIdPrefix
from database.repos.products import ProductsRepo

router = Router(name=__file__)


@router.message(Command(SlashCommand.SHOP))
async def open_shop_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=ShopStates.list)


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith(ProductIdPrefix)),
    MagicData(F.command.args.as_("product_deeplink")),
)
async def open_product_by_deeplink(
    message: Message,
    product_deeplink: str,
    dialog_manager: DialogManager,
    products_repo: FromDishka[ProductsRepo],
) -> None:
    product_id = product_deeplink[len(ProductIdPrefix):]
    if product_id.isdigit():
        product_id = ProductId(int(product_id))
        product = await products_repo.get_by_id(product_id)
        if product and product.stock > 0:
            await dialog_manager.start(
                ShopStates.one,
                data={"product_id": product_id},
            )
