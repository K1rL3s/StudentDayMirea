from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.handlers.admin.broadcast.states import BroadcastStates
from bot.handlers.admin.lottery.states import LotteryStartInputStates
from bot.handlers.admin.secrets.view.states import ViewSecretsStates
from bot.handlers.admin.shop.view.states import ViewProductsStates
from bot.handlers.admin.tasks.view.states import ViewTasksStates
from bot.handlers.admin.users.view.states import ViewUserStates


async def on_go_to_broadcast(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=BroadcastStates.wait)


async def on_go_to_secrets(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=ViewSecretsStates.list)


async def on_go_to_view_users(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=ViewUserStates.id)


async def on_go_to_tasks(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=ViewTasksStates.list)


async def on_go_to_shop(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=ViewProductsStates.list)


async def on_go_to_lottery(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=LotteryStartInputStates.user_id)
