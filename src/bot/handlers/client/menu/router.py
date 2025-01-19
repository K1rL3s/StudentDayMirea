from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot.enums import SlashCommand
from bot.stickers import PANDA_WINK

from .states import MenuStates

router = Router(name=__file__)


@router.message(Command(SlashCommand.MENU, SlashCommand.START, SlashCommand.CANCEL))
async def menu_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await message.answer_sticker(sticker=PANDA_WINK)
    await dialog_manager.start(state=MenuStates.menu)
