from aiogram import F, Router
from aiogram.filters import CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from core.ids import ProductId
from core.services.qrcodes import ProductIdPrefix
from database.repos.products import ProductsRepo

from .view.states import ViewProductsStates

router = Router(name=__file__)


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
    if not product_id.isdigit():
        product_id = ProductId(int(product_id))
        if await products_repo.get_by_id(product_id):
            await dialog_manager.start(
                ViewProductsStates.one,
                data={"product_id": product_id},
            )
