from dishka import Provider, Scope, provide

from database.repos.logs import LogsRepo
from database.repos.products import ProductsRepo
from database.repos.purchases import PurchasesRepo
from database.repos.secrets import SecretsRepo
from database.repos.tasks import TasksRepo
from database.repos.tickets import TicketsRepo
from database.repos.users import UsersRepo


class ReposProvider(Provider):
    scope = Scope.REQUEST

    logs_repo = provide(LogsRepo)
    products_repo = provide(ProductsRepo)
    purchases_repo = provide(PurchasesRepo)
    users_repo = provide(UsersRepo)
    secrets_repo = provide(SecretsRepo)
    tasks_repo = provide(TasksRepo)
    tickets_repo = provide(TicketsRepo)
