from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.secrets.create.states import CreateSecretStates
from bot.handlers.admin.secrets.edit.states import EditSecretStates
from bot.handlers.admin.secrets.view.states import ViewSecretsStates
from core.ids import SecretId
from core.services.secrets import SecretsService
from database.models import UserModel


async def on_secret_selected(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    dialog_manager.dialog_data["secret_id"] = item_id
    await dialog_manager.next()


async def on_create_secret(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=CreateSecretStates.phrase)


async def on_delete_secret(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.next()


async def on_edit_phrase(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    secret_id: SecretId = dialog_manager.dialog_data["secret_id"]
    await dialog_manager.start(
        state=EditSecretStates.phrase,
        data={"secret_id": secret_id},
    )


async def on_edit_reward(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    secret_id: SecretId = dialog_manager.dialog_data["secret_id"]
    await dialog_manager.start(
        state=EditSecretStates.reward,
        data={"secret_id": secret_id},
    )


async def on_edit_activation_limit(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    secret_id: SecretId = dialog_manager.dialog_data["secret_id"]
    await dialog_manager.start(
        state=EditSecretStates.activation_limit,
        data={"secret_id": secret_id},
    )


@inject
async def on_confirm_delete_secret(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
    secrets_service: FromDishka[SecretsService],
) -> None:
    secret_id: SecretId = dialog_manager.dialog_data["secret_id"]
    admin: UserModel = dialog_manager.middleware_data["user"]
    await secrets_service.delete(secret_id, admin.id)
    await dialog_manager.start(state=ViewSecretsStates.list)
