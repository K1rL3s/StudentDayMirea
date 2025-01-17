from sqlalchemy import select

from core.ids import TicketId, UserId
from database.models.lottery import TicketModel
from database.repos.base import BaseAlchemyRepo


class TicketsRepo(BaseAlchemyRepo):
    async def get_by_id(self, ticket_id: TicketId) -> TicketModel | None:
        query = select(TicketModel).where(TicketModel.id == ticket_id)
        return await self.session.scalar(query)

    async def get_by_user_id(self, user_id: UserId) -> TicketModel | None:
        query = select(TicketModel).where(TicketModel.user_id == user_id)
        return await self.session.scalar(query)

    async def get_all(self) -> list[TicketModel]:
        query = select(TicketModel)
        return list(await self.session.scalars(query))

    async def create(
        self,
        ticket_id: TicketId,
        user_id: UserId,
        fio: str,
        group: str,
    ) -> TicketModel:
        ticket = TicketModel(id=ticket_id, user_id=user_id, fio=fio, group=group)
        self.session.add(ticket)
        await self.session.flush()
        return ticket
