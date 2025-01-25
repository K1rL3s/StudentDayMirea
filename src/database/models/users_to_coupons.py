from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.ids import CouponId, UserId
from database.models._mixins import CreatedAtMixin
from database.models.base import BaseAlchemyModel


class UserToCouponModel(CreatedAtMixin, BaseAlchemyModel):
    __tablename__ = "user_to_coupon"

    user_id: Mapped[UserId] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
        unique=True,
    )
    coupon_id: Mapped[CouponId] = mapped_column(
        ForeignKey("coupons.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
        unique=True,
    )
