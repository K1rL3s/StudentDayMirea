from sqlalchemy import delete, select, update

from core.ids import TaskId, UserId
from database.models import TaskModel, UsersToTasksModel
from database.repos.base import BaseAlchemyRepo


class TasksRepo(BaseAlchemyRepo):
    async def get_by_id(self, task_id: TaskId) -> TaskModel | None:
        query = select(TaskModel).where(TaskModel.id == task_id)
        return await self.session.scalar(query)

    async def get_all(self) -> list[TaskModel]:
        query = select(TaskModel).order_by(TaskModel.id.asc())
        return list(await self.session.scalars(query))

    async def create(
        self,
        title: str,
        description: str,
        reward: int,
        answer: str,
    ) -> TaskModel:
        task = TaskModel(
            title=title,
            description=description,
            reward=reward,
            answer=answer,
        )
        self.session.add(task)
        await self.session.flush()
        return task

    async def delete(self, task_id: TaskId) -> None:
        query = delete(TaskModel).where(TaskModel.id == task_id)
        await self.session.execute(query)
        await self.session.flush()

    async def link_user_to_task(
        self,
        user_id: UserId,
        task_id: TaskId,
        status: bool = False,
    ) -> None:
        user_to_task = UsersToTasksModel(
            user_id=user_id,
            task_id=task_id,
            status=status,
        )
        self.session.add(user_to_task)
        await self.session.flush()

    async def unlink_user_from_task(self, user_id: UserId, task_id: TaskId) -> None:
        query = delete(UsersToTasksModel).where(
            UsersToTasksModel.user_id == user_id,
            UsersToTasksModel.task_id == task_id,
        )
        await self.session.execute(query)
        await self.session.flush()

    async def set_status(self, task_id: TaskId, status: bool) -> None:
        query = update(TaskModel).where(TaskModel.id == task_id).values(status=status)
        await self.session.execute(query)
        await self.session.flush()

    async def set_users_to_tasks_status(
        self,
        user_id: UserId,
        task_id: TaskId,
        status: bool,
    ) -> None:
        query = (
            update(UsersToTasksModel)
            .where(
                UsersToTasksModel.user_id == user_id,
                UsersToTasksModel.task_id == task_id,
            )
            .values(status=status)
        )
        await self.session.execute(query)
        await self.session.flush()

    async def is_task_reward_claimed(
        self,
        user_id: UserId,
        task_id: TaskId,
    ) -> bool:
        query = select(UsersToTasksModel).where(
            UsersToTasksModel.user_id == user_id,
            UsersToTasksModel.task_id == task_id,
        )
        relation = await self.session.scalar(query)
        return relation and relation.status

    async def set_qrcode_image_id(self, task_id: TaskId, image_id: str) -> None:
        query = (
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(qrcode_image_id=image_id)
        )
        await self.session.execute(query)
        await self.session.flush()

    async def get_active_task(self, user_id: UserId) -> TaskModel | None:
        subquery = select(UsersToTasksModel.task_id).where(
            UsersToTasksModel.user_id == user_id,
            UsersToTasksModel.status == False,  # noqa: E712
        )
        query = select(TaskModel).where(TaskModel.id == subquery.as_scalar())
        return await self.session.scalar(query)
