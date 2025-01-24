from aiogram import Router
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from dishka import FromDishka

from core.ids import UserId
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def block_bot(
    event: ChatMemberUpdated,
    user_id: UserId,
    users_repo: FromDishka[UsersRepo],
) -> None:
    await users_repo.change_active(user_id, False)
