from aiogram import F, Router
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.filters import Command, CommandObject, CommandStart, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.filters.roles import IsAdmin
from bot.handlers.admin.users.view.states import ViewUserStates
from core.ids import UserId
from core.services.qrcodes import UserIdPrefix
from database.repos.coupons import CouponsRepo
from database.repos.tickets import TicketsRepo
from database.repos.users import UsersRepo

router = Router(name=__file__)


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith(UserIdPrefix)),
    MagicData(F.command.args.as_("user_deeplink")),
)
async def open_user_by_deeplink(
    message: Message,
    user_deeplink: str,
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    user_id = user_deeplink[len(UserIdPrefix):]
    if not user_id.isdigit():
        raise CancelHandler

    user = await users_repo.get_by_id(UserId(int(user_id)))
    if user is None:
        await message.answer(f"Юзер c ID {user_id} не найден")
        return

    await dialog_manager.start(state=ViewUserStates.one, data={"view_user_id": user.id})


@router.message(Command("delete"), IsAdmin())
async def delete_user(
    message: Message,
    command: CommandObject,
    users_repo: FromDishka[UsersRepo],
) -> None:
    if command.args and command.args.isdigit():
        return await users_repo.delete(UserId(int(command.args)))

    text = "Формат: /delete <user_id>"
    await message.answer(text=text)
    return None


@router.message(Command("clear"), IsAdmin())
async def clear_lottery_user(
    message: Message,
    command: CommandObject,
    tickets_repo: FromDishka[TicketsRepo],
    coupons_repo: FromDishka[CouponsRepo],
) -> None:
    if command.args and command.args.isdigit():
        user_id = UserId(int(command.args))
        await tickets_repo.delete(user_id)
        await coupons_repo.delete_relation(user_id=user_id, coupon_id=None)
        return

    text = "Формат: /clear <user_id>"
    await message.answer(text=text)
    return
