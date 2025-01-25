from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.ids import CouponId
from database.models._mixins import CreatedAtMixin
from database.models.base import BaseAlchemyModel


class CouponModel(CreatedAtMixin, BaseAlchemyModel):
    __tablename__ = "coupons"

    id: Mapped[CouponId] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
