from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.enums import SlashCommand
from bot.handlers.client.menu.states import MenuStates
from core.services.qrcode_saver import QRCodeSaver
from database.models import UserModel

router = Router(name=__file__)


@router.message(Command(SlashCommand.ID))
async def show_my_id_as_qrcode(
    message: Message,
    dialog_manager: DialogManager,
    user: UserModel,
    qrcode_saver: FromDishka[QRCodeSaver],
) -> None:
    text = f"Покажи это организатору =)\n\nID: <code>{user.id}</code>"

    if user.qrcode_image_id:
        await message.answer_photo(photo=user.qrcode_image_id, caption=text)
    else:
        await qrcode_saver.user(text, user.id, message.from_user.id)

    await dialog_manager.start(state=MenuStates.menu)
