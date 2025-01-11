from typing import Any

from aiogram.filters import Filter

from core.enums import RightsRole
from database.models import UserModel


class RoleAccess(Filter):
    def __init__(self, roles: list[RightsRole]) -> None:
        self.roles = roles

    async def __call__(
        self,
        _: Any,
        user: UserModel,
    ) -> bool:
        return user.role in self.roles


class IsAdmin(RoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.ADMIN])


class IsSeller(RoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.SELLER, RightsRole.ADMIN])


class IsStager(RoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.STAGER, RightsRole.ADMIN])


class IsLottery(RoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.LOTTERY, RightsRole.ADMIN])


class IsWithRole(RoleAccess):
    def __init__(self) -> None:
        super().__init__(RightsRole.values())
