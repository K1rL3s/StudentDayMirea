from aiogram import Dispatcher

from .cancel import router as cancel_router
from .cart.dialogs import cart_dialog
from .cart.router import router as purchases_router
from .help.dialogs import help_dialog
from .help.router import router as help_router
from .menu.dialogs import menu_dialog
from .menu.router import router as menu_router
from .qrcode.router import router as qrcodes_router
from .secret.router import router as secret_router
from .shop.dialogs import shop_dialog
from .shop.router import router as products_router

# from bot.handlers.seller.router import router as seller_router
# from bot.handlers.stages.router import router as stages_router
from .start.dialogs import start_dialog
from .start.router import router as start_router
from .transfer_funds.dialogs import transfer_dialog
from .transfer_funds.router import router as transfer_funds_router


def include_client_routers(dp: Dispatcher) -> None:
    dp.include_routers(  # TODO: проверить порядок роутеров
        start_router,
        cancel_router,
        secret_router,
        menu_router,
        help_router,
        qrcodes_router,
        products_router,
        purchases_router,
        transfer_funds_router,
        # seller_router,
        # stages_router,
    )
    _include_client_dialogs(dp)


# Регистрация диалогов после роутеров чтобы дефолт команды не перехватывались диалогами
def _include_client_dialogs(dp: Dispatcher) -> None:
    dp.include_routers(
        start_dialog,
        help_dialog,
        menu_dialog,
        shop_dialog,
        cart_dialog,
        transfer_dialog,
    )
