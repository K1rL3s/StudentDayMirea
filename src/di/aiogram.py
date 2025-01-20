from aiogram import Bot
from aiogram.types import TelegramObject
from dishka import Provider, Scope, provide


class AiogramBotProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def bot(self, event: TelegramObject) -> Bot:
        return event.bot
