from dataclasses import dataclass

from sqlalchemy import delete, select

from core.ids import ProductId, UserId
from database.models import ProductModel, PurchaseModel
from database.repos.base import BaseAlchemyRepo


@dataclass
class PurchasesInfo:
    total_products: int
    total_purchases: int
    product_to_quantity: list[tuple[tuple[ProductId, str], int]]
    formated_info: str


class PurchasesRepo(BaseAlchemyRepo):
    async def create(
        self,
        user_id: UserId,
        product_id: ProductId,
        quantity: int,
    ) -> PurchaseModel:
        purchase = PurchaseModel(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
        )
        self.session.add(purchase)
        await self.session.flush()
        return purchase

    async def get_user_purchases(
        self,
        user_id: UserId,
    ) -> list[tuple[ProductModel, PurchaseModel]]:
        query = (
            select(ProductModel, PurchaseModel)
            .join(PurchaseModel, PurchaseModel.product_id == ProductModel.id)
            .where(PurchaseModel.user_id == user_id)
            .order_by(ProductModel.price.asc())
        )
        return list(await self.session.execute(query))

    async def clear_purchases(
        self,
        user_id: UserId,
        product_ids: list[ProductId],
    ) -> None:
        query = delete(PurchaseModel).where(
            PurchaseModel.user_id == user_id,
            PurchaseModel.product_id.in_(product_ids),
        )
        await self.session.execute(query)
        await self.session.flush()

    @staticmethod
    def format_purchases(
        purchases: list[tuple[ProductModel, PurchaseModel]],
    ) -> PurchasesInfo:
        total_products = len({i[0].id for i in purchases})
        total_purchases = sum(i[1].quantity for i in purchases)

        product_to_quantity: dict[tuple[ProductId, str], int] = {}
        for product, purchase in purchases:
            if (product.id, product.name) not in product_to_quantity:
                product_to_quantity[(product.id, product.name)] = 0
            product_to_quantity[(product.id, product.name)] += purchase.quantity

        sorted_product_to_quntity = sorted(
            product_to_quantity.items(),
            key=lambda x: x[0][0],
        )
        formated_purchases = "\n".join(
            f"<b>{product_name}</b>: {quantity}"
            for (product_id, product_name), quantity in sorted_product_to_quntity
        )

        return PurchasesInfo(
            total_products,
            total_purchases,
            sorted_product_to_quntity,
            formated_purchases,
        )
