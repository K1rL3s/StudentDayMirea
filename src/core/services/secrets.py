from sqlalchemy.exc import IntegrityError

from core.exceptions import (
    ActivationLimitReached,
    InvalidValue,
    SecretAlreadyExists,
    SecretNotFound,
    SecretRewardAlreadyClaimed,
    UserNotFound,
)
from core.ids import SecretId, UserId
from core.services.roles import RolesService
from database.repos.logs import LogsRepo
from database.repos.secrets import SecretsRepo
from database.repos.users import UsersRepo


class SecretsService:
    def __init__(
        self,
        secrets_repo: SecretsRepo,
        users_repo: UsersRepo,
        logs_repo: LogsRepo,
        role_service: RolesService,
    ) -> None:
        self.secrets_repo = secrets_repo
        self.users_repo = users_repo
        self.logs_repo = logs_repo
        self.role_service = role_service

    async def reward_for_secret(self, user_id: UserId, phrase: str) -> int:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        secret = await self.secrets_repo.get_by_phrase(phrase)
        if secret is None:
            raise SecretNotFound(phrase)

        if not await self.secrets_repo.is_activation_available(
            secret.id,
            secret.activation_limit,
        ):
            raise ActivationLimitReached

        if await self.secrets_repo.is_secret_claimed(user_id, secret.id):
            raise SecretRewardAlreadyClaimed(user_id, secret.id)

        await self.secrets_repo.link_user_to_secret(user_id, secret.id)

        new_balance = user.balance + secret.reward
        await self.users_repo.set_balance(user_id, new_balance)

        await self.logs_repo.log_action(
            user_id,
            f"Reward {secret.reward} coins for secret {secret.id} id",
        )

        return secret.reward

    async def create(
        self,
        phrase: str,
        reward: int,
        activation_limit: int,
        master_id: UserId,
    ) -> SecretId:
        await self.role_service.is_admin(master_id)

        if not phrase:
            raise InvalidValue("Секретная фраза не может быть пустой")
        if reward < 0:
            raise InvalidValue("Награда должна быть больше нуля")
        if activation_limit < 0:
            raise InvalidValue("Количество активаций должно быть больше нуля")

        try:
            secret = await self.secrets_repo.create(phrase, reward, activation_limit)
        except IntegrityError as e:  # TODO убрать отсюда импорт ошибки алхимии?
            raise SecretAlreadyExists(phrase) from e

        return secret.id

    async def delete(self, secret_id: SecretId, master_id: UserId) -> None:
        await self.role_service.is_admin(master_id)
        await self.secrets_repo.delete(secret_id)
