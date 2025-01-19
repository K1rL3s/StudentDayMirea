from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.secrets.view.states import ViewSecretsStates
from core.ids import UserId
from core.services.secrets import SecretsService


async def secret_phrase_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    phrase = message.text.strip()
    dialog_manager.dialog_data["phrase"] = phrase
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def secret_reward_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    reward = int(message.text.strip())
    dialog_manager.dialog_data["reward"] = reward
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def secret_activation_limit_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    activation_limit = int(message.text.strip())
    dialog_manager.dialog_data["activation_limit"] = activation_limit
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


@inject
async def confirm_create_secret(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    secrets_service: FromDishka[SecretsService],
) -> None:
    phrase: str = dialog_manager.dialog_data["phrase"]
    reward: int = dialog_manager.dialog_data["reward"]
    activation_limit: int = dialog_manager.dialog_data["activation_limit"]
    creator_id: UserId = dialog_manager.middleware_data["user_id"]
    secret_id = await secrets_service.create(
        phrase,
        reward,
        activation_limit,
        creator_id,
    )

    dialog_manager.dialog_data["secret_id"] = secret_id
    await dialog_manager.start(
        state=ViewSecretsStates.one,
        data={"secret_id": secret_id},
    )
