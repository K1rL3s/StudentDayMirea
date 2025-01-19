from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.ids import QuestId, UserId
from database.models import QuestModel, UserModel
from database.models._mixins import CreatedAtMixin, UpdatedAtMixin
from database.models.base import BaseAlchemyModel


class UsersToQuestsModel(CreatedAtMixin, UpdatedAtMixin, BaseAlchemyModel):
    __tablename__ = "users_to_quests"

    user_id: Mapped[UserId] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    quest_id: Mapped[QuestId] = mapped_column(
        ForeignKey("quests.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # False - не выполнено, True - выполнено
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user: Mapped[UserModel] = relationship(
        "UserModel",
        cascade="all,delete",
    )
    quest: Mapped[QuestModel] = relationship(
        "QuestModel",
        cascade="all,delete",
    )
