from core.exceptions import UserNotFound
from core.ids import ProductId, UserId
from core.services.products import ProductsService
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
        products_service: ProductsService,
    ) -> None:
        self.purchases_repo = purchases_repo
        self.users_repo = users_repo
        self.logs_repo = logs_repo
        self.roles_service = roles_service
        self.products_service = products_service

    async def clear_cart(
        self,
        slave_id: UserId,
        product_ids: list[ProductId],
        master_id: UserId,
    ) -> None:
        await self.roles_service.is_seller(master_id)

        user = await self.users_repo.get_by_id(slave_id)
        if user is None:
            raise UserNotFound(slave_id)

        await self.purchases_repo.clear_purchases(slave_id, product_ids)

        await self.logs_repo.log_action(slave_id, f"Cart clean by {master_id=}")

    async def refund(
        self,
        user_id: UserId,
        product_ids: list[ProductId],
    ) -> None:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        refund_money = 0
        for product_id in product_ids:
            refund_money += await self._refund_one_product(user_id, product_id)

        await self.purchases_repo.clear_purchases(user_id, product_ids)

        new_balance = user.balance + refund_money
        await self.users_repo.set_balance(user_id, new_balance)

    async def _refund_one_product(self, user_id: UserId, product_id: ProductId) -> int:
        purchases = await self.purchases_repo.get_user_purchases_by_product_id(
            user_id,
            product_id,
        )
        quantity = sum(purchase.quantity for _, purchase in purchases)
        return await self.products_service.refund(product_id, quantity)
