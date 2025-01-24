from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.ids import QuestId, UserId
from database.models._mixins import CreatedAtMixin, UpdatedAtMixin
from database.models.base import BaseAlchemyModel


class UsersToQuestsModel(CreatedAtMixin, UpdatedAtMixin, BaseAlchemyModel):
    __tablename__ = "users_to_quests"

    user_id: Mapped[UserId] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    quest_id: Mapped[QuestId] = mapped_column(
        ForeignKey("quests.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )

    # False - не выполнено, True - выполнено
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
