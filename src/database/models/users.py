from sqlalchemy import BigInteger, Boolean, Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.ids import TgId, UserId
from database.models._mixins import CreatedAtMixin, UpdatedAtMixin
from database.models.base import BaseAlchemyModel


class UserModel(CreatedAtMixin, UpdatedAtMixin, BaseAlchemyModel):
    __tablename__ = "users"

    id: Mapped[UserId] = mapped_column(
        Integer,
        Identity(start=1000),
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    tg_id: Mapped[TgId] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True,
        index=True,
    )
    name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[str | None] = mapped_column(String(16), default=None, nullable=True)

    qrcode_image_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        unique=True,
    )
