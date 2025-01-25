from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.ids import SecretId
from database.models._mixins import CreatedAtMixin
from database.models.base import BaseAlchemyModel


class SecretModel(CreatedAtMixin, BaseAlchemyModel):
    __tablename__ = "secrets"

    id: Mapped[SecretId] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    phrase: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
    )
    reward: Mapped[int] = mapped_column(Integer, nullable=False)
    activation_limit: Mapped[int] = mapped_column(Integer, nullable=False)
