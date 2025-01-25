from bot.utils.answer import format_answer
from core.exceptions import (
    ActiveTaskNotFound,
    TaskNotFound,
    TaskRewardAlreadyClaimed,
    UserNotFound,
    WrongTaskAnswer,
)
from core.ids import TaskId, UserId
from core.services.roles import RolesService
from database.models import TaskModel
from database.repos.logs import LogsRepo
from database.repos.tasks import TasksRepo
from database.repos.users import UsersRepo


class TasksService:
    def __init__(
        self,
        tasks_repo: TasksRepo,
        users_repo: UsersRepo,
        logs_repo: LogsRepo,
        roles_service: RolesService,
    ) -> None:
        self.tasks_repo = tasks_repo
        self.users_repo = users_repo
        self.logs_repo = logs_repo
        self.roles_service = roles_service

    async def create(
        self,
        title: str,
        description: str,
        reward: int,
        answer: str,
        master_id: UserId,
    ) -> TaskId:
        await self.roles_service.is_stager(master_id)

        task_id = await self.tasks_repo.create(title, description, reward, answer)

        await self.logs_repo.log_action(master_id, f"Create {task_id=}")

        return task_id

    async def delete(self, task_id: TaskId, master_id: UserId) -> None:
        await self.roles_service.is_stager(master_id)

        await self.tasks_repo.delete(task_id)

        await self.logs_repo.log_action(master_id, f"Delete {task_id=}")

    async def start(self, task_id: TaskId, user_id: UserId) -> TaskModel:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        new_task = await self.tasks_repo.get_by_id(task_id)
        if new_task is None:
            raise TaskNotFound(task_id)

        old_task = await self.tasks_repo.get_active_task(user_id)
        if old_task:
            await self.tasks_repo.unlink_user_from_task(user_id, task_id)

        await self.tasks_repo.link_user_to_task(user_id, task_id, status=False)

        await self.logs_repo.log_action(user_id, f"Start {task_id=}")

        return new_task

    async def cancel_active_task(self, user_id: UserId) -> None:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        task = await self.tasks_repo.get_active_task(user_id)
        if task is None:
            raise ActiveTaskNotFound(user_id)

        await self.logs_repo.log_action(user_id, f"Cancel {task.id=}")

        await self.tasks_repo.unlink_user_from_task(user_id, task.id)

    async def reward_for_task_by_pharse(
        self,
        user_id: UserId,
        phrase: str,
    ) -> tuple[str, int]:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        task = await self.tasks_repo.get_active_task(user_id)
        if task is None:
            raise ActiveTaskNotFound(user_id)

        if await self.tasks_repo.is_task_reward_claimed(user_id, task.id):
            raise TaskRewardAlreadyClaimed(user_id, task.id)

        if format_answer(phrase) != format_answer(task.answer):
            raise WrongTaskAnswer

        await self.tasks_repo.set_users_to_tasks_status(user_id, task.id, True)

        new_balance = user.balance + task.reward
        await self.users_repo.set_balance(user_id, new_balance)

        await self.logs_repo.log_action(user_id, f"Reward {task.id=} by phrase")

        return task.title, task.reward

    async def reward_for_task_by_stager(
        self,
        slave_id: UserId,
        master_id: UserId,
    ) -> tuple[str, int]:
        user = await self.users_repo.get_by_id(slave_id)
        if user is None:
            raise UserNotFound(slave_id)

        await self.roles_service.is_stager(master_id)

        task = await self.tasks_repo.get_active_task(slave_id)
        if task is None:
            raise ActiveTaskNotFound(slave_id)

        await self.tasks_repo.set_users_to_tasks_status(slave_id, task.id, True)

        new_balance = user.balance + task.reward
        await self.users_repo.set_balance(slave_id, new_balance)

        await self.logs_repo.log_action(
            slave_id,
            f"Reward {task.id=} by stager {master_id=}",
        )

        return task.title, task.reward
