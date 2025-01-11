from aiogram import Router

from bot.filters.roles import IsAdmin, IsLottery, IsSeller, IsStager, IsWithRole

from .broadcast.dialogs import broadcast_dialog
from .broadcast.router import router as broadcast_router
from .logs.router import router as logs_router
from .money.router import router as money_router
from .panel.dialogs import admin_panel_dialog
from .panel.router import router as admin_panel_router
from .secrets.dialogs import create_secret_dialog, view_secrets_dialog
from .secrets.router import router as secrets_router
from .shop.dialogs import create_product_dialog, view_products_dialog
from .shop.router import router as products_routes
from .tasks.create.dialogs import create_task_dialog
from .tasks.router import router as tasks_router
from .tasks.view.dialogs import view_tasks_dialog
from .users.cart.dialogs import user_cart_dialog
from .users.lottery.dialogs import set_lottery_info_dialog
from .users.role.dialogs import user_role_dialog
from .users.router import router as users_router
from .users.task import cancel_task_dialog, confirm_task_dialog, view_user_task_dialog
from .users.view.dialogs import view_user_dialog


def include_admin_routers(root_router: Router) -> None:
    admin_router = Router(name=__file__)
    for observer in admin_router.observers.values():
        observer.filter(IsAdmin())
    admin_router.include_routers(
        broadcast_router,
        logs_router,
        money_router,
        secrets_router,
    )

    seller_router = Router(name=__file__)
    for observer in seller_router.observers.values():
        observer.filter(IsSeller())
    seller_router.include_routers(products_routes)

    stager_router = Router(name=__file__)
    for observer in stager_router.observers.values():
        observer.filter(IsStager())
    stager_router.include_routers(tasks_router)

    with_role_router = Router(name=__file__)
    for observer in with_role_router.observers.values():
        observer.filter(IsWithRole())
    with_role_router.include_routers(
        admin_panel_router,
        admin_router,
        seller_router,
        stager_router,
        users_router,
    )

    root_router.include_router(with_role_router)


def include_admin_dialogs(root_router: Router) -> None:
    admin_router = Router(name=__file__)
    for observer in admin_router.observers.values():
        observer.filter(IsAdmin())
    admin_router.include_routers(
        broadcast_dialog,
        view_secrets_dialog,
        create_secret_dialog,
        user_role_dialog,
    )

    seller_router = Router(name=__file__)
    for observer in seller_router.observers.values():
        observer.filter(IsSeller())
    seller_router.include_routers(
        user_cart_dialog,
        view_products_dialog,
        create_product_dialog,
    )

    stager_router = Router(name=__file__)
    for observer in stager_router.observers.values():
        observer.filter(IsStager())
    stager_router.include_routers(
        view_tasks_dialog,
        create_task_dialog,
        view_user_task_dialog,
        cancel_task_dialog,
        confirm_task_dialog,
    )

    lottery_router = Router(name=__file__)
    for observer in stager_router.observers.values():
        observer.filter(IsLottery())
    lottery_router.include_routers(set_lottery_info_dialog)

    with_role_router = Router(name=__file__)
    for observer in with_role_router.observers.values():
        observer.filter(IsWithRole())
    with_role_router.include_routers(
        admin_panel_dialog,
        view_user_dialog,
        admin_router,
        seller_router,
        stager_router,
        lottery_router,
    )

    root_router.include_router(with_role_router)
