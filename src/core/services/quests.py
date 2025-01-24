from core.exceptions import (
    QuestNotFound,
    QuestNotKnown,
    QuestRewardAlreadyClaimed,
    UserNotFound,
    WrongQuestAnswer,
)
from core.final_quest import FINAL_QUEST_ID
from core.ids import QuestId, UserId
from core.services.roles import RolesService
from database.models import QuestModel
from database.repos.logs import LogsRepo
from database.repos.quests import QuestsRepo
from database.repos.users import UsersRepo


class QuestsService:
    def __init__(
        self,
        quests_repo: QuestsRepo,
        users_repo: UsersRepo,
        logs_repo: LogsRepo,
        roles_service: RolesService,
    ) -> None:
        self.quests_repo = quests_repo
        self.users_repo = users_repo
        self.logs_repo = logs_repo
        self.roles_service = roles_service

    async def create(
        self,
        order: int,
        title: str,
        description: str,
        task: str,
        image_id: str | None,
        reward: int,
        answer: str,
        end_hint: str,
        right_answer: str,
        wrong_answer: str,
        master_id: UserId,
    ) -> QuestId:
        await self.roles_service.is_stager(master_id)
        quest = await self.quests_repo.create(
            order=order,
            title=title,
            description=description,
            task=task,
            image_id=image_id,
            reward=reward,
            answer=answer,
            end_hint=end_hint,
            right_answer=right_answer,
            wrong_answer=wrong_answer,
        )
        return quest.id

    async def delete(self, quest_id: QuestId, master_id: UserId) -> None:
        await self.roles_service.is_stager(master_id)
        if quest_id != FINAL_QUEST_ID:
            await self.quests_repo.delete(quest_id)

    async def start(self, quest_id: QuestId, user_id: UserId) -> QuestModel:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        quest = await self.quests_repo.get_by_id(quest_id)
        if quest is None:
            raise QuestNotFound(quest_id)

        await self.quests_repo.link_user_to_quest(user_id, quest_id)

        return quest

    async def reward_for_quest_by_pharse(
        self,
        quest_id: QuestId,
        user_id: UserId,
        phrase: str,
    ) -> tuple[str, int]:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        quest = await self.quests_repo.get_by_id(quest_id)
        if quest is None:
            raise QuestNotFound(quest_id)

        if not await self.quests_repo.is_user_know_quest(user_id, quest_id):
            raise QuestNotKnown(user_id, quest_id)

        if await self.quests_repo.is_quest_reward_claimed(user_id, quest_id):
            raise QuestRewardAlreadyClaimed(user_id, quest_id)

        if phrase.casefold() != quest.answer.casefold():
            raise WrongQuestAnswer

        await self.quests_repo.set_users_to_quests_status(user_id, quest.id, True)

        new_balance = user.balance + quest.reward
        await self.users_repo.set_balance(user_id, new_balance)

        if await self.is_final_quest_available(user_id):
            await self.start(FINAL_QUEST_ID, user_id)

        return quest.title, quest.reward

    async def is_final_quest_available(self, user_id: UserId) -> bool:
        known_quests = await self.quests_repo.get_known_quests(user_id)
        all_quests = await self.quests_repo.get_all()
        return (
            len(known_quests) != 0  # что-то должно быть найдено
            and len(known_quests) == len(all_quests) - 1  # без учёта финального
            and all(pair[1].status for pair in known_quests)  # все найденное выполнено
        )
