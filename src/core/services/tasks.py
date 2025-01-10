from core.exceptions import (
    ActiveTaskNotFound,
    TaskInactive,
    TaskNotFound,
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
        end_phrase: str,
        creator_id: UserId,
    ) -> TaskId:
        await self.roles_service.is_stager(creator_id)
        task = await self.tasks_repo.create(title, description, reward, end_phrase)
        return task.id

    async def delete(self, task_id: TaskId, master_id: UserId) -> None:
        await self.roles_service.is_stager(master_id)
        await self.tasks_repo.delete(task_id)

    async def start(self, task_id: TaskId, user_id: UserId) -> TaskModel:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        new_task = await self.tasks_repo.get_by_id(task_id)
        if new_task is None:
            raise TaskNotFound(task_id)
        if not new_task.status:  # Задание деактивировано
            raise TaskInactive(new_task.id)

        old_task = await self.tasks_repo.get_active_task(user_id)
        if old_task:
            await self.tasks_repo.unlink_user_from_task(user_id, task_id)

        await self.tasks_repo.link_user_to_task(user_id, task_id, status=False)

        return new_task

    async def cancel_active_task(self, user_id: UserId) -> None:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        task = await self.tasks_repo.get_active_task(user_id)
        if task is None:
            raise ActiveTaskNotFound(user_id)

        await self.tasks_repo.unlink_user_from_task(user_id, task.id)

    async def reward_for_active_task(self, user_id: UserId, phrase: str) -> int:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        task = await self.tasks_repo.get_active_task(user_id)
        if task is None:
            raise ActiveTaskNotFound(user_id)

        if phrase != task.end_phrase:
            raise WrongTaskAnswer

        await self.tasks_repo.set_users_to_tasks_status(user_id, task.id, True)

        new_balance = user.balance + task.reward
        await self.users_repo.set_balance(user_id, new_balance)

        return task.reward
