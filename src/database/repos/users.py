from sqlalchemy import select, update

from core.ids import TgId, UserId
from database.models import UserModel
from database.repos.base import BaseAlchemyRepo


class UsersRepo(BaseAlchemyRepo):
    async def create(
        self,
        tg_id: TgId,
        name: str | None = None,
        balance: int = 0,
        role: str | None = None,
    ) -> UserModel:
        user = UserModel(tg_id=tg_id, name=name, role=role, balance=balance)
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(self, user_id: UserId, name: str, role: str | None) -> None:
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                name=name,
                role=role,
            )
        )
        await self.session.execute(query)
        await self.session.flush()

    async def get_by_id(self, user_id: UserId) -> UserModel | None:
        query = select(UserModel).where(UserModel.id == user_id)
        return await self.session.scalar(query)

    async def get_by_tg_id(self, tg_id: TgId) -> UserModel | None:
        query = select(UserModel).where(UserModel.tg_id == tg_id)
        return await self.session.scalar(query)

    async def get_active(self) -> list[UserModel]:
        query = (
            select(UserModel)
            .where(UserModel.is_active == True)  # noqa: E712
            .order_by(UserModel.created_at.asc())
        )
        return list(await self.session.scalars(query))

    async def set_balance(self, tg_id: UserId, new_balance: int) -> None:
        query = (
            update(UserModel).where(UserModel.id == tg_id).values(balance=new_balance)
        )
        await self.session.execute(query)
        await self.session.flush()

    async def change_active(self, tg_id: UserId, is_active: bool) -> None:
        query = (
            update(UserModel).where(UserModel.id == tg_id).values(is_active=is_active)
        )
        await self.session.execute(query)
        await self.session.flush()

    async def set_qrcode_image_id(self, tg_id: UserId, qrcode_image_id: str) -> None:
        query = (
            update(UserModel)
            .where(UserModel.id == tg_id)
            .values(qrcode_image_id=qrcode_image_id)
        )
        await self.session.execute(query)
        await self.session.flush()

    async def set_role(self, tg_id: UserId, role: str | None) -> None:
        query = update(UserModel).where(UserModel.id == tg_id).values(role=role)
        await self.session.execute(query)
        await self.session.flush()
