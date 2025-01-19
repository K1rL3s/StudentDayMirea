from aiogram import F, Router
from aiogram.filters import MagicData

from .cancel import router as cancel_router
from .cart.dialogs import cart_dialog
from .cart.router import router as purchases_router
from .help.dialogs import help_dialog
from .help.router import router as help_router
from .lottery.dialogs import lottery_dialog
from .menu.dialogs import menu_dialog
from .menu.router import router as menu_router
from .qrcode.router import router as qrcodes_router
from .quest.dialogs import quest_answer_dialog, view_quests_dialog
from .quest.start.router import router as quest_start_router
from .secret.router import router as secret_router
from .shop.dialogs import shop_dialog
from .shop.router import router as products_router
from .start.dialogs import start_dialog
from .start.router import router as start_router
from .task.dialogs import start_task_dialog, task_answer_dialog, view_task_dialog
from .task.router import router as task_router
from .transfer_funds.dialogs import transfer_dialog
from .transfer_funds.router import router as transfer_funds_router


def include_register_routers(root_router: Router) -> None:
    root_router.include_routers(
        start_router,
        start_dialog,
    )


def include_client_routers(root_router: Router) -> None:
    # фильтр на имя чтобу у новых юзеров не было доступа кроме регистрации
    registered_clients_router = Router(name=__file__)
    for observer in registered_clients_router.observers.values():
        observer.filter(MagicData(F.user.name))

    registered_clients_router.include_routers(
        cancel_router,
        task_router,
        products_router,
        quest_start_router,
        secret_router,
        menu_router,
        help_router,
        qrcodes_router,
        purchases_router,
        transfer_funds_router,
    )

    root_router.include_routers(registered_clients_router)


def include_client_dialogs(root_router: Router) -> None:
    # фильтр на имя чтобу у новых юзеров не было доступа ко всему кроме регистрации
    registered_clients_router = Router(name=__file__)
    for observer in registered_clients_router.observers.values():
        observer.filter(MagicData(F.user.name))

    root_router.include_routers(
        help_dialog,
        menu_dialog,
        shop_dialog,
        cart_dialog,
        transfer_dialog,
        lottery_dialog,
        view_task_dialog,
        start_task_dialog,
        task_answer_dialog,
        view_quests_dialog,
        quest_answer_dialog,
    )
