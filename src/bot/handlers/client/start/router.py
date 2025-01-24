from aiogram import F, Router
from aiogram.filters import CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode

from .states import StartStates

router = Router(name=__file__)


@router.message(CommandStart(), ~MagicData(F.user.name))
async def start_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        state=StartStates.name,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
