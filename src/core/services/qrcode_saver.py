from io import BytesIO
from uuid import uuid4

from aiogram import Bot
from aiogram.types import BufferedInputFile

from core.ids import ProductId, QuestId, TaskId, TgId, UserId
from core.services.qrcodes import QRCodeService
from database.repos.products import ProductsRepo
from database.repos.quests import QuestsRepo
from database.repos.tasks import TasksRepo
from database.repos.users import UsersRepo


class QRCodeSaver:
    def __init__(
        self,
        qrcode_service: QRCodeService,
        products_repo: ProductsRepo,
        tasks_repo: TasksRepo,
        quests_repo: QuestsRepo,
        users_repo: UsersRepo,
        bot: Bot,
    ) -> None:
        self.qrcode_service = qrcode_service
        self.products_repo = products_repo
        self.tasks_repo = tasks_repo
        self.quests_repo = quests_repo
        self.users_repo = users_repo
        self.bot = bot

    async def user(
        self,
        caption: str,
        save_to: UserId,
        send_to: TgId,
    ) -> None:
        qrcode = self.qrcode_service.user_id_qrcode(save_to)
        qrcode_image_id = await self._send(caption, send_to, qrcode)
        await self.users_repo.set_qrcode_image_id(save_to, qrcode_image_id)

    async def task(
        self,
        caption: str,
        task_id: TaskId,
        send_to: TgId,
    ) -> None:
        qrcode = self.qrcode_service.task_id_qrcode(task_id)
        qrcode_image_id = await self._send(caption, send_to, qrcode)
        await self.tasks_repo.set_qrcode_image_id(task_id, qrcode_image_id)

    async def product(
        self,
        caption: str,
        product_id: ProductId,
        send_to: TgId,
    ) -> None:
        qrcode = self.qrcode_service.product_id_qrcode(product_id)
        qrcode_image_id = await self._send(caption, send_to, qrcode)
        await self.products_repo.set_qrcode_image_id(product_id, qrcode_image_id)

    async def quest(
        self,
        caption: str,
        quest_id: QuestId,
        send_to: TgId,
    ) -> None:
        qrcode = self.qrcode_service.quest_id_qrcode(quest_id)
        qrcode_image_id = await self._send(caption, send_to, qrcode)
        await self.quests_repo.set_qrcode_image_id(quest_id, qrcode_image_id)

    async def _send(self, caption: str, send_to: TgId, qrcode: BytesIO) -> str:
        photo = BufferedInputFile(qrcode.getvalue(), f"qrcode_{uuid4()!s}.png")
        bot_message = await self.bot.send_photo(
            chat_id=send_to,
            photo=photo,
            caption=caption,
        )
        return bot_message.photo[-1].file_id
