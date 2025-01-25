from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.ids import LogId, UserId
from database.models._mixins import CreatedAtMixin
from database.models.base import BaseAlchemyModel


class LogsModel(CreatedAtMixin, BaseAlchemyModel):
    __tablename__ = "logs"

    id: Mapped[LogId] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[UserId] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(String(4096), nullable=False)
