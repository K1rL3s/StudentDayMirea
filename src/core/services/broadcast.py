import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramNotFound

from core.ids import TgId, UserId
from core.services.roles import RolesService
from database.models import UserModel
from database.repos.users import UsersRepo

logger = logging.getLogger(__name__)

NOTIFIES_PER_BATCH = 15


@dataclass
class BroadcastResult:
    ok: int
    fail: int

    @property
    def total(self) -> int:
        return self.ok + self.fail


class Broadcaster:
    def __init__(
        self,
        bot: Bot,
        users_repo: UsersRepo,
        roles_service: RolesService,
    ) -> None:
        self.bot = bot
        self.users_repo = users_repo
        self.roles_service = roles_service

    async def broadcast(self, message: str, master_id: UserId) -> BroadcastResult:
        await self.roles_service.is_admin(master_id)

        users = await self.users_repo.get_active()
        return await self._broadcast(message, users)

    async def _broadcast(
        self,
        text: str,
        users: list[UserModel],
    ) -> BroadcastResult:
        ok = 0
        for i in range(0, len(users), NOTIFIES_PER_BATCH):
            tasks = [
                asyncio.create_task(self.one_notify(text, user.id, user.tg_id))
                for user in users[i : i + NOTIFIES_PER_BATCH]
            ]
            timer = asyncio.create_task(asyncio.sleep(1))
            results = await asyncio.gather(*tasks)
            await timer

            ok += sum(results)

        return BroadcastResult(ok, len(users) - ok)

    async def one_notify(
        self,
        text: str,
        user_id: UserId,
        tg_id: TgId,
        **kwargs: Any,
    ) -> bool:
        try:
            await self.bot.send_message(text=text, chat_id=tg_id, **kwargs)
        except (TelegramNotFound, TelegramForbiddenError):
            await self.users_repo.change_active(user_id, is_active=False)
            return False
        except Exception as e:  # noqa: BLE001
            logging.warning(f"Ошибка во время рассылки: {type(e).__name__}('{e}')")
            return False

        logger.debug("Уведомление успешно для ID=%d", user_id)
        return True
