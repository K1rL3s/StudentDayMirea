from core.exceptions import (
    InvalidValue,
    NotEnoughMoney,
    NotEnoughStock,
    ProductNotFound,
    UserNotFound,
)
from core.ids import ProductId, UserId
from core.services.roles import RolesService
from database.repos.logs import LogsRepo
from database.repos.products import ProductsRepo
from database.repos.purchases import PurchasesRepo
from database.repos.users import UsersRepo


class ProductsService:
    def __init__(
        self,
        products_repo: ProductsRepo,
        users_repo: UsersRepo,
        purchases_repo: PurchasesRepo,
        logs_repo: LogsRepo,
        roles_service: RolesService,
    ) -> None:
        self.products_repo = products_repo
        self.users_repo = users_repo
        self.purchases_repo = purchases_repo
        self.logs_repo = logs_repo
        self.roles_service = roles_service

    async def buy_product(
        self,
        user_id: UserId,
        product_id: ProductId,
        quantity: int,
    ) -> int:
        product = await self.products_repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        if product.stock < quantity:
            raise NotEnoughStock(product.stock, quantity)

        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        total_price = product.price * quantity
        if user.balance < total_price:
            raise NotEnoughMoney(user.balance, total_price)

        await self.purchases_repo.create(user.id, product_id, quantity)

        new_balance = user.balance - total_price
        await self.users_repo.set_balance(user.id, new_balance)

        new_stock = product.stock - quantity
        await self.set_stock(product_id, new_stock)

        await self.logs_repo.log_action(
            user.id,
            f"Bought {product_id} for {quantity} units",
        )

        return new_balance

    async def set_stock(self, product_id: ProductId, new_stock: int) -> int:
        if new_stock < 0:
            raise InvalidValue("Кол-во товара не может быть отрицательным")

        product = await self.products_repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        return await self.products_repo.set_stock(product_id, new_stock)

    async def set_price(self, product_id: ProductId, new_price: int) -> int:
        if new_price <= 0:
            raise InvalidValue("Цена не может быть отрицательной")

        product = await self.products_repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        return await self.products_repo.set_price(product_id, new_price)

    async def create(
        self,
        name: str,
        description: str,
        price: int,
        stock: int,
        master_id: UserId,
    ) -> ProductId:
        await self.roles_service.is_seller(master_id)

        return await self.products_repo.create_product(name, description, price, stock)

    async def delete(self, product_id: ProductId, master_id: UserId) -> None:
        await self.roles_service.is_seller(master_id)

        product = await self.products_repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        await self.products_repo.delete(product_id)
