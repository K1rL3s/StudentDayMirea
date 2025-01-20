import random
import string

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.ids import QuestId
from database.models._mixins import CreatedAtMixin, UpdatedAtMixin
from database.models.base import BaseAlchemyModel

QUEST_ID_LEN = 8


def quest_id_generator() -> QuestId:
    return QuestId(
        "".join(random.choices(string.ascii_letters + string.digits, k=QUEST_ID_LEN)),
    )


class QuestModel(CreatedAtMixin, UpdatedAtMixin, BaseAlchemyModel):
    __tablename__ = "quests"

    id: Mapped[QuestId] = mapped_column(
        String(length=QUEST_ID_LEN),
        primary_key=True,
        default=quest_id_generator,
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(2048), nullable=False)
    task: Mapped[str] = mapped_column(String(1024), nullable=False)
    image_id: Mapped[str] = mapped_column(String(128), nullable=True)
    reward: Mapped[int] = mapped_column(Integer, nullable=False)
    answer: Mapped[str] = mapped_column(String(256), nullable=False)
    end_hint: Mapped[str] = mapped_column(String(256), nullable=False)

    qrcode_image_id: Mapped[str] = mapped_column(String(128), nullable=True)
