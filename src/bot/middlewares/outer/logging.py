import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import REJECTED, UNHANDLED
from aiogram.types import CallbackQuery, Message, TelegramObject

from core.ids import TgId, UserId

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    @staticmethod
    def get_short_info(user_id: UserId, tg_id: TgId) -> str | None:
        return f"{user_id=} {tg_id=}"

    async def pre_callbackquery(self, callback: CallbackQuery, user_id: UserId) -> None:
        logger.info(
            'Get callback=%s "%s" [%s]',
            callback.id,
            callback.data,
            self.get_short_info(user_id, TgId(callback.from_user.id)),
        )

    async def post_callbackquery(
        self,
        callback: CallbackQuery,
        user_id: UserId,
        is_handled: bool,
    ) -> None:
        logger.info(
            'Over=%s callback=%s "%s" [%s]',
            is_handled,
            callback.id,
            callback.data,
            self.get_short_info(user_id, TgId(callback.from_user.id)),
        )

    async def pre_message(self, message: Message, user_id: UserId) -> None:
        if message.photo:
            log = 'Get photo=%d "%s" [%s]'
            text = " ".join(message.caption.split()) if message.caption else ""
        else:
            log = 'Get message=%d "%s" [%s]'
            text = " ".join(message.text.split())
        logger.info(
            log,
            message.message_id,
            text,
            self.get_short_info(user_id, TgId(message.from_user.id)),
        )

    async def post_message(
        self,
        message: Message,
        user_id: UserId,
        is_handled: bool,
    ) -> None:
        if message.photo:
            log = 'Over=%s photo=%d "%s" [%s]'
            text = " ".join(message.caption.split()) if message.caption else ""
        else:
            log = 'Over=%s message=%d "%s" [%s]'
            text = " ".join(message.text.split())
        logger.info(
            log,
            is_handled,
            message.message_id,
            text,
            self.get_short_info(user_id, TgId(message.from_user.id)),
        )

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_id: UserId = data["user_id"]
        class_name = event.__class__.__name__.lower()

        await getattr(self, f"pre_{class_name}")(event, user_id)

        result = await handler(event, data)
        is_handled = result not in (UNHANDLED, REJECTED)

        await getattr(self, f"post_{class_name}")(event, user_id, is_handled)

        return result
