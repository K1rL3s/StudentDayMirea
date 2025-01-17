from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from dishka import FromDishka

from core.ids import UserId
from core.services.users import UsersService

router = Router(name=__file__)


@router.message(Command("money"), StateFilter(None))
async def admin_update_money(
    message: Message,
    command: CommandObject,
    user_id: UserId,
    users_service: FromDishka[UsersService],
) -> None:
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        slave_id, amount = int(args[0]), int(args[1])
        await users_service.update_balance(slave_id, user_id, amount)
        await message.answer(f"Добавлено {amount} пользователю {slave_id}")
    else:
        await message.answer("Формат: /money <user_id> <amount>", parse_mode=None)
