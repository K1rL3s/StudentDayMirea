from core.exceptions import (
    InvalidValue,
    InvalidValueAfterUpdate,
    NotAdmin,
    NotEnoughMoney,
    UserNotFound,
)
from database.repos.logs import LogsRepo
from database.repos.users import UsersRepo


class UsersService:
    def __init__(
        self,
        users_repo: UsersRepo,
        logs_repo: LogsRepo,
    ) -> None:
        self.users_repo = users_repo
        self.logs_repo = logs_repo

    async def admin_update_balance(
        self,
        slave_id: int,
        master_id: int,
        amount: int,
    ) -> int:
        user = await self.users_repo.get_by_id(slave_id)
        if user is None:
            raise UserNotFound(slave_id)

        admin = await self.users_repo.get_by_id(master_id)
        if admin is None:
            raise UserNotFound(master_id)
        if not admin.is_admin:
            raise NotAdmin(master_id)

        if user.balance + amount < 0:  # если отнимаем
            raise InvalidValueAfterUpdate(
                f"Баланс станет отрицательным. Текущий: {user.balance}",
            )

        new_balance = user.balance + amount
        await self.users_repo.set_balance(slave_id, new_balance)

        await self.logs_repo.log_action(
            master_id,
            f"Added money {amount} to user {slave_id}",
        )

        return new_balance

    async def admin_set_balance(
        self,
        slave_id: int,
        master_id: int,
        new_balance: int,
    ) -> int:
        if new_balance < 0:
            raise InvalidValue("Новый баланс не может быть отрицательным")

        user = await self.users_repo.get_by_id(slave_id)
        if user is None:
            raise UserNotFound(slave_id)

        admin = await self.users_repo.get_by_id(master_id)
        if admin is None:
            raise UserNotFound(master_id)
        if not admin.is_admin:
            raise NotAdmin(master_id)

        await self.users_repo.set_balance(slave_id, new_balance)

        await self.logs_repo.log_action(
            master_id,
            f"Set {new_balance} money to user {slave_id}",
        )
        await self.logs_repo.log_action(
            slave_id,
            f"Set {new_balance} money from user {master_id}",
        )

        return new_balance

    async def transfer_funds(
        self,
        sender_id: int,
        receiver_id: int,
        amount: int,
    ) -> int:
        if amount <= 0:
            raise InvalidValue("Нельзя передать 0 или меньше денег")

        sender = await self.users_repo.get_by_id(sender_id)
        if sender is None:
            raise UserNotFound(sender_id)

        if sender.balance < amount:
            raise NotEnoughMoney(sender.balance, amount)

        receiver = await self.users_repo.get_by_id(receiver_id)
        if receiver is None:
            raise UserNotFound(receiver_id)

        new_sender_balance = sender.balance - amount
        await self.users_repo.set_balance(sender_id, new_sender_balance)

        new_receiver_balance = receiver.balance + amount
        await self.users_repo.set_balance(receiver_id, new_receiver_balance)

        await self.logs_repo.log_action(
            sender_id,
            f"Transferred {amount} to user {sender_id}",
        )
        await self.logs_repo.log_action(
            receiver_id,
            f"Received {amount} from user {sender_id}",
        )

        return new_sender_balance

    async def change_stage(self, tg_id: int, stage: int) -> None:
        user = await self.users_repo.get_by_id(tg_id)
        if not user:
            raise UserNotFound(tg_id)

        await self.users_repo.change_stage(tg_id, stage)
