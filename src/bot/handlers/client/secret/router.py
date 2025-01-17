from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.dialogs.flags import FORCE_GET_USER_KEY
from bot.enums import SlashCommand
from bot.handlers.client.menu.states import MenuStates
from core.ids import UserId
from core.services.secrets import SecretsService

router = Router(name=__file__)


@router.message(Command(SlashCommand.SECRET))
async def check_secret_handler(
    message: Message,
    command: CommandObject,
    user_id: UserId,
    dialog_manager: DialogManager,
    secrets_service: FromDishka[SecretsService],
) -> None:
    if secret_phrase := command.args.strip():
        reward = await secrets_service.reward_for_secret(user_id, secret_phrase)
        if reward is not None:
            await message.answer(f"🕵 Секрет найден! Начислено {reward} Пятаков 💰")
            await dialog_manager.start(
                state=MenuStates.menu,
                data={FORCE_GET_USER_KEY: None},
            )
