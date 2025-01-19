from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert

from core.ids import QuestId, UserId
from database.models import QuestModel, UsersToQuestsModel
from database.repos.base import BaseAlchemyRepo


class QuestsRepo(BaseAlchemyRepo):
    async def get_by_id(self, quest_id: QuestId) -> QuestModel | None:
        query = select(QuestModel).where(QuestModel.id == quest_id)
        return await self.session.scalar(query)

    async def get_all(self) -> list[QuestModel]:
        query = select(QuestModel).order_by(QuestModel.order.asc())
        return list(await self.session.scalars(query))

    async def get_known_quests(
        self,
        user_id: UserId,
    ) -> list[tuple[QuestModel, UsersToQuestsModel]]:
        query = (
            select(QuestModel, UsersToQuestsModel)
            .join(
                UsersToQuestsModel,
                QuestModel.id == UsersToQuestsModel.quest_id,
                isouter=True,
            )
            .where(UsersToQuestsModel.user_id == user_id)
        )
        results = await self.session.execute(query)
        return list(results.all())

    async def get_user_to_quest(
        self,
        quest_id: QuestId,
        user_id: UserId,
    ) -> UsersToQuestsModel | None:
        query = select(UsersToQuestsModel).where(
            UsersToQuestsModel.quest_id == quest_id,
            UsersToQuestsModel.user_id == user_id,
        )
        return await self.session.scalar(query)

    async def create(
        self,
        order: int,
        title: str,
        description: str,
        task: str,
        image_id: str | None,
        reward: int,
        answer: str,
    ) -> QuestModel:
        quest = QuestModel(
            order=order,
            title=title,
            description=description,
            task=task,
            image_id=image_id,
            reward=reward,
            answer=answer,
        )
        self.session.add(quest)
        await self.session.flush()
        return quest

    async def delete(self, quest_id: QuestId) -> None:
        query = delete(QuestModel).where(QuestModel.id == quest_id)
        await self.session.execute(query)
        await self.session.flush()

    async def link_user_to_quest(
        self,
        user_id: UserId,
        quest_id: QuestId,
    ) -> None:
        query = (
            insert(UsersToQuestsModel)
            .values(
                user_id=user_id,
                quest_id=quest_id,
                status=False,
            )
            .on_conflict_do_nothing(
                index_elements=[
                    UsersToQuestsModel.user_id,
                    UsersToQuestsModel.quest_id,
                ],
            )
        )
        await self.session.execute(query)
        await self.session.flush()

    async def set_users_to_quests_status(
        self,
        user_id: UserId,
        quest_id: QuestId,
        status: bool,
    ) -> None:
        query = (
            update(UsersToQuestsModel)
            .where(
                UsersToQuestsModel.user_id == user_id,
                UsersToQuestsModel.quest_id == quest_id,
            )
            .values(status=status)
        )
        await self.session.execute(query)
        await self.session.flush()

    async def is_quest_reward_claimed(
        self,
        user_id: UserId,
        quest_id: QuestId,
    ) -> bool:
        query = select(UsersToQuestsModel).where(
            UsersToQuestsModel.user_id == user_id,
            UsersToQuestsModel.quest_id == quest_id,
        )
        relation = await self.session.scalar(query)
        return relation and relation.status

    async def set_qrcode_image_id(self, quest_id: QuestId, image_id: str) -> None:
        query = (
            update(QuestModel)
            .where(QuestModel.id == quest_id)
            .values(qrcode_image_id=image_id)
        )
        await self.session.execute(query)
        await self.session.flush()

    async def is_user_know_quest(self, user_id: UserId, quest_id: QuestId) -> bool:
        query = select(UsersToQuestsModel).where(
            UsersToQuestsModel.user_id == user_id,
            UsersToQuestsModel.quest_id == quest_id,
        )
        relation = await self.session.scalar(query)
        return relation is not None
