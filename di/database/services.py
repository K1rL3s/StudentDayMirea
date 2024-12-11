from dishka import Provider, Scope, provide

from core.services.products import ProductsService
from core.services.users import UsersService


class ServicesProvider(Provider):
    products_service = provide(ProductsService, scope=Scope.REQUEST)
    users_service = provide(UsersService, scope=Scope.REQUEST)
