from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dishka import FromDishka

from core.ids import UserId
from database.repos.logs import LogsRepo

router = Router(name=__file__)


@router.message(Command("logs"))
async def admin_view_logs(
    message: Message,
    command: CommandObject,
    logs_repo: FromDishka[LogsRepo],
) -> None:
    if command.args and len(command.args.split()) == 1:
        user_id = UserId(int(command.args.strip()))
        logs = await logs_repo.get_user_logs(user_id)
        log_texts = [f"{log.created_at}: {log.description}" for log in logs][:10]
        await message.answer("\n\n".join(log_texts) or "Нет логов")
    else:
        await message.answer("Формат: /logs <user_id>", parse_mode=None)
