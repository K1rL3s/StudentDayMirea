from sqlalchemy import delete, select, update

from core.ids import ProductId
from database.models.products import ProductModel
from database.repos.base import BaseAlchemyRepo


class ProductsRepo(BaseAlchemyRepo):
    async def create_product(
        self,
        name: str,
        description: str,
        price: int,
        stock: int,
    ) -> ProductId:
        product = ProductModel(
            name=name,
            description=description,
            price=price,
            stock=stock,
        )
        self.session.add(product)
        await self.session.flush()
        return product.id

    async def get_by_id(self, product_id: ProductId) -> ProductModel | None:
        query = select(ProductModel).where(ProductModel.id == product_id)
        return await self.session.scalar(query)

    async def get_available(self) -> list[ProductModel]:
        query = (
            select(ProductModel)
            .where(ProductModel.stock > 0)
            .order_by(ProductModel.price.asc(), ProductModel.name.asc())
        )
        return list(await self.session.scalars(query))

    async def get_all(self) -> list[ProductModel]:
        query = select(ProductModel).order_by(
            ProductModel.price.asc(),
            ProductModel.name.asc(),
        )
        return list(await self.session.scalars(query))

    async def set_stock(self, product_id: ProductId, new_stock: int) -> int:
        query = (
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(stock=new_stock)
        )
        await self.session.execute(query)
        await self.session.flush()
        return new_stock

    async def set_price(self, product_id: ProductId, new_price: int) -> int:
        query = (
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(price=new_price)
        )
        await self.session.execute(query)
        await self.session.flush()
        return new_price

    async def delete(self, product_id: ProductId) -> None:
        query = delete(ProductModel).where(ProductModel.id == product_id)
        await self.session.execute(query)
        await self.session.flush()

    async def set_qrcode_image_id(self, product_id: ProductId, image_id: str) -> None:
        query = (
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(qrcode_image_id=image_id)
        )
        await self.session.execute(query)
        await self.session.flush()
