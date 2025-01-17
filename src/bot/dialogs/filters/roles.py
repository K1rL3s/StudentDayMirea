from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common.when import Whenable

from core.enums import RightsRole
from database.models import UserModel


class DialogsRoleAccess:
    def __init__(self, roles: list[RightsRole]) -> None:
        self.roles = roles

    def __call__(
        self,
        data: dict[str, Any],
        widget: Whenable,
        dialog_manager: DialogManager,
    ) -> bool:
        user: UserModel = data["middleware_data"]["user"]
        return user.role in self.roles


class IsAdmin(DialogsRoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.ADMIN])


class IsSeller(DialogsRoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.SELLER, RightsRole.ADMIN])


class IsStager(DialogsRoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.STAGER, RightsRole.ADMIN])


class IsLottery(DialogsRoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.LOTTERY, RightsRole.ADMIN])


class IsWithRole(DialogsRoleAccess):
    def __init__(self) -> None:
        super().__init__(RightsRole.values())
