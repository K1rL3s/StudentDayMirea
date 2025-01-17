from aiogram import Router
from aiogram_dialog import setup_dialogs
from aiogram_dialog.context.media_storage import MediaIdStorage
from aiogram_dialog.manager.message_manager import MessageManager

from ..dialogs.dialog_manager import MyManagerFactory
from .admin import include_admin_dialogs, include_admin_routers
from .client import (
    include_client_dialogs,
    include_client_routers,
    include_register_routers,
)
from .exceptions import router as exceptions_router


def include_routers(root_router: Router) -> None:
    include_admin_routers(root_router)
    include_client_routers(root_router)
    include_register_routers(root_router)
    include_admin_dialogs(root_router)
    include_client_dialogs(root_router)
    root_router.include_routers(exceptions_router)

    manager_factory = MyManagerFactory(
        message_manager=MessageManager(),
        media_id_storage=MediaIdStorage(),
    )
    setup_dialogs(root_router, dialog_manager_factory=manager_factory)
