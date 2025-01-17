from sqlalchemy.exc import IntegrityError

from core.exceptions import TicketAlreadyExists
from core.ids import TicketId, UserId
from core.services.roles import RolesService
from database.models.lottery import TicketModel
from database.repos.tickets import TicketsRepo


class TicketsService:
    def __init__(self, tickets_repo: TicketsRepo, roles_service: RolesService) -> None:
        self.tickets_repo = tickets_repo
        self.roles_service = roles_service

    async def create(
        self,
        ticket_id: TicketId,
        user_id: UserId,
        fio: str,
        group: str,
        master_id: UserId,
    ) -> TicketModel:
        await self.roles_service.is_lottery(master_id)

        if await self.tickets_repo.get_by_id(ticket_id):
            raise TicketAlreadyExists.ticket(ticket_id)

        if await self.tickets_repo.get_by_user_id(ticket_id):
            raise TicketAlreadyExists.user(user_id)

        try:
            return await self.tickets_repo.create(ticket_id, user_id, fio, group)
        except IntegrityError as e:
            raise TicketAlreadyExists.unknown(ticket_id, user_id) from e
