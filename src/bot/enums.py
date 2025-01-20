from tools.enums import StrEnum


class SlashCommand(StrEnum):
    START = "start"
    HELP = "help"
    MENU = "menu"
    SHOP = "shop"
    CART = "cart"
    TRANSFER = "transfer"
    ADMIN = "admin"
    SECRET = "secret"
    ID = "id"
    TASK = "task"
    QUEST = "quest"


class TextCommand(StrEnum):
    START = "Старт"
    HELP = "Помощь"
    MENU = "Меню"
    SHOP = "Магазин"
    CART = "Корзина"
    TRANSFER = "Перевод"
    ADMIN = "Админ"
    CANCEL = "Отмена"


class BotWindow(StrEnum):
    MENU = "menu"
    HELP = "help"
    ADMIN_PANEL = "admin_panel"
    SHOP = "shop"
    CART = "cart"
    TRANSFER = "transfer"
    TASK = "task"
