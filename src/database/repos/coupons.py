from typing import cast

from sqlalchemy import delete, func, or_, select

from core.ids import CouponId, UserId
from database.models import UserModel, UserToCouponModel
from database.models.coupons import CouponModel
from database.repos.base import BaseAlchemyRepo


class CouponsRepo(BaseAlchemyRepo):
    async def create(self, description: str) -> CouponId:
        coupon = CouponModel(description=description)
        self.session.add(coupon)
        await self.session.flush()
        return coupon.id

    async def link_user_to_random_coupon(self, user_id: UserId) -> CouponId | None:
        query = (
            select(CouponModel.id)
            .outerjoin(
                UserToCouponModel,
                UserToCouponModel.coupon_id == CouponModel.id,
            )
            .where(UserToCouponModel.coupon_id == None)  # noqa: E711
            .order_by(func.random())
            .limit(1)
        )

        coupon_id = cast(CouponId | None, await self.session.scalar(query))
        if coupon_id is not None:
            new_user_to_coupon = UserToCouponModel(user_id=user_id, coupon_id=coupon_id)
            self.session.add(new_user_to_coupon)
            await self.session.flush()

        return coupon_id

    async def delete(self, coupon_id: CouponId) -> None:
        query = delete(CouponModel).where(CouponModel.id == coupon_id)
        await self.session.execute(query)
        await self.session.flush()

    async def delete_relation(
        self,
        user_id: UserId | None,
        coupon_id: CouponId | None,
    ) -> None:
        query = delete(UserToCouponModel).where(
            or_(
                UserToCouponModel.user_id == user_id,
                UserToCouponModel.coupon_id == coupon_id,
            )
        )
        await self.session.execute(query)
        await self.session.flush()

    async def get_by_id(
        self,
        coupon_id: CouponId,
    ) -> tuple[CouponModel, UserModel | None] | None:
        query = (
            select(CouponModel, UserModel)
            .outerjoin(UserToCouponModel, UserToCouponModel.coupon_id == CouponModel.id)
            .outerjoin(UserModel, UserToCouponModel.user_id == UserModel.id)
            .where(CouponModel.id == coupon_id)
        )
        result = await self.session.execute(query)
        row = result.one()
        return row if row else None

    async def get_by_user_id(self, user_id: UserId) -> CouponModel | None:
        query = select(CouponModel).where(
            CouponModel.id
            == select(UserToCouponModel.coupon_id)
            .where(
                UserToCouponModel.user_id == user_id,
            )
            .scalar_subquery(),
        )
        return await self.session.scalar(query)

    async def get_all(self) -> list[CouponModel]:
        query = select(CouponModel).order_by(CouponModel.id.asc())
        return list(await self.session.scalars(query))
