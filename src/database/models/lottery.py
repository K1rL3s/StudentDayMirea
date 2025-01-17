from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.ids import TicketId, UserId
from database.models.base import BaseAlchemyModel


class TicketModel(BaseAlchemyModel):
    __tablename__ = "lottery_tickets"

    id: Mapped[TicketId] = mapped_column(Integer, primary_key=True)
    fio: Mapped[str] = mapped_column(String(256), nullable=False)
    group: Mapped[str] = mapped_column(String(32), nullable=False)
    user_id: Mapped[UserId] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )
