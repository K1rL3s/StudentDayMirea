import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, MenuButtonCommands

from bot.config import BotConfig
from bot.enums import SlashCommand


async def set_commands(bot: Bot) -> None:
    commands: dict[str, str] = {
        SlashCommand.START: "Старт",
        SlashCommand.MENU: "Меню",
        SlashCommand.HELP: "Помощь",
        SlashCommand.SHOP: "Товары в наличии",
        SlashCommand.CART: "Купленные товары",
        SlashCommand.QUEST: "Квест",
        SlashCommand.TASK: "Текущее задание",
        SlashCommand.TRANSFER: "Перевод другу",
        SlashCommand.SECRET: "Секрет ;)",
    }

    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in commands.items()
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )


async def on_startup(bot: Bot) -> None:
    await set_commands(bot)
    user = await bot.me()
    logging.info(
        "Start polling for bot @%s id=%d - '%s'",
        user.username,
        user.id,
        user.full_name,
    )


async def on_shutdown(bot: Bot) -> None:
    user = await bot.me()
    logging.info(
        "Stop polling for bot @%s id=%d - '%s'",
        user.username,
        user.id,
        user.full_name,
    )


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher(
        storage=MemoryStorage(),
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
        name="__main__",
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    return dp


def create_bot(bot_config: BotConfig, parse_mode: ParseMode = ParseMode.HTML) -> Bot:
    return Bot(
        token=bot_config.bot_token,
        default=DefaultBotProperties(
            parse_mode=parse_mode,
            link_preview_is_disabled=True,
        ),
    )
