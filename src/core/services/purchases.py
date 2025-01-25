from core.exceptions import UserNotFound
from core.ids import ProductId, UserId
from core.services.roles import RolesService
from database.repos.logs import LogsRepo
from database.repos.purchases import PurchasesRepo
from database.repos.users import UsersRepo


class PurchasesService:
    def __init__(
        self,
        purchases_repo: PurchasesRepo,
        users_repo: UsersRepo,
        logs_repo: LogsRepo,
        roles_service: RolesService,
    ) -> None:
        self.purchases_repo = purchases_repo
        self.users_repo = users_repo
        self.logs_repo = logs_repo
        self.roles_service = roles_service

    async def clear_cart(
        self,
        slave_id: UserId,
        product_ids: list[ProductId],
        master_id: UserId,
    ) -> None:
        user = await self.users_repo.get_by_id(slave_id)
        if user is None:
            raise UserNotFound(slave_id)

        await self.roles_service.is_seller(master_id)

        await self.purchases_repo.clear_purchases(slave_id, product_ids)

        await self.logs_repo.log_action(slave_id, f"Cart clean by {master_id=}")
