from aiogram import F, Router
from aiogram.filters import Command, CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.enums import SlashCommand
from bot.handlers.client.shop.states import ShopStates
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
async def start_task_by_deeplink(
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
                ShopStates.one,
                data={"product_id": product_id},
            )

    await message.delete()
