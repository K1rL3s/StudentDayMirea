from core.exceptions import UserNotFound
from core.ids import UserId
from core.services.roles import RolesService
from database.repos.tickets import TicketsRepo
from database.repos.users import UsersRepo


class TicketsService:
    def __init__(
        self,
        tickets_repo: TicketsRepo,
        users_repo: UsersRepo,
        roles_service: RolesService,
    ) -> None:
        self.tickets_repo = tickets_repo
        self.users_repo = users_repo
        self.roles_service = roles_service

    async def create_or_update(
        self,
        user_id: UserId,
        fio: str,
        group: str,
        master_id: UserId,
    ) -> None:
        await self.roles_service.is_lottery(master_id)

        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        ticket = await self.tickets_repo.get_by_user_id(user_id)
        if ticket:
            return await self.tickets_repo.update(user_id, fio, group)

        return await self.tickets_repo.create(user_id, fio, group)
