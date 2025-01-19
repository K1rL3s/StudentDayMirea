from typing import Any

from bot.translate import translate_role
from core.enums import ALL_ROLES


async def get_roles(**__: Any) -> dict[str, Any]:
    return {"roles": list(enumerate(translate_role(role) for role in ALL_ROLES))}
