from aiogram.types import TelegramObject
from dishka import Provider, Scope, provide

from core.services.broadcast import Broadcaster
from core.services.products import ProductsService
from core.services.purchases import PurchasesService
from core.services.qrcode_saver import QRCodeSaver
from core.services.qrcodes import QRCodeService
from core.services.roles import RolesService
from core.services.secrets import SecretsService
from core.services.tasks import TasksService
from core.services.tickets import TicketsService
from core.services.users import UsersService


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def qrcode_service(self, event: TelegramObject) -> QRCodeService:
        bot = event.bot
        bot_name = (await bot.me()).username
        return QRCodeService(bot_name)

    qrcode_saver = provide(QRCodeSaver)
    broadcaster = provide(Broadcaster)
    products_service = provide(ProductsService)
    users_service = provide(UsersService)
    secrets_service = provide(SecretsService)
    tasks_service = provide(TasksService)
    purchases_service = provide(PurchasesService)
    roles_service = provide(RolesService)
    tickets_service = provide(TicketsService)
