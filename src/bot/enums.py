from tools.enums import StrEnum


class SlashCommand(StrEnum):
    START = "start"
    HELP = "help"
    MENU = "menu"
    SHOP = "shop"
    CART = "cart"
    TRANSFER = "transfer"
    ADMIN = "admin"
    PANEL = "panel"
    BROADCAST = "broadcast"
    SECRET = "secret"
    SECRETS = "secrets"
    CANCEL = "cancel"
    ID = "id"
    TASKS = "tasks"
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
