import contextlib
import logging

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Chat, ErrorEvent, ReplyKeyboardRemove
from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent

from bot.handlers.client.menu.states import MenuStates
from bot.handlers.client.start.states import StartStates
from core.exceptions import ServiceException
from database.models import UserModel

router = Router(name=__file__)


@router.error(ExceptionTypeFilter(ServiceException))
async def service_exceptions_handler(
    event: ErrorEvent,
    bot: Bot,
    event_chat: Chat,
) -> None:
    e = event.exception

    logging.warning(f"{e.__class__.__name__} {e!s}")
    text = f"😵‍💫 Произошла ошибка, попробуй ещё раз. Вот её текст:\n\n{e!s}"
    await bot.send_message(chat_id=event_chat.id, text=text)

    raise event.exception  # чтобы откатывалась сессия алхимии


@router.error(ExceptionTypeFilter(UnknownIntent))
async def on_unknown_intent(
    event: ErrorEvent,
    dialog_manager: DialogManager,
    user: UserModel,
) -> None:
    logging.error("Restarting dialog: %s", event.exception)

    if event.update.callback_query:
        if event.update.callback_query.message:
            with contextlib.suppress(TelegramBadRequest):
                await event.update.callback_query.message.delete()
    elif event.update.message:
        await event.update.message.answer(
            text="😵‍💫",
            reply_markup=ReplyKeyboardRemove(),
        )

    if user.name:
        await dialog_manager.start(state=MenuStates.menu)
    else:
        await dialog_manager.start(state=StartStates.name)


@router.error(ExceptionTypeFilter(Exception))
async def all_exceptions_handler(
    event: ErrorEvent,
    bot: Bot,
    event_chat: Chat,
) -> None:
    text = "❌😵 Произошла ошибка...\nПопробуй ещё раз или напиши ему -> @K1rLes"
    await bot.send_message(chat_id=event_chat.id, text=text)

    raise event.exception
