from aiogram import Bot
from aiogram.types import BufferedInputFile

from core.ids import ProductId, UserId
from core.services.qrcodes import QRCodeService
from database.repos.products import ProductsRepo


async def send_and_save_product_qrcode(
    qrcode_service: QRCodeService,
    products_repo: ProductsRepo,
    caption: str,
    bot: Bot,
    product_id: ProductId,
    send_to: UserId,
) -> None:
    qrcode = qrcode_service.product_qrcode(product_id)
    photo = BufferedInputFile(qrcode.getvalue(), f"qrcode_product{product_id}.png")
    bot_message = await bot.send_photo(chat_id=send_to, photo=photo, caption=caption)
    qrcode_image_id = bot_message.photo[-1].file_id
    await products_repo.set_qrcode_image_id(product_id, qrcode_image_id)
