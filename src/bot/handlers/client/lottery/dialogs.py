from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToMenuButton

from .getters import get_lottery_info
from .states import ViewLotteryStates

LOTTERY_USERS_TEXT = """
🎟️ В лотерее сейчас участвует {total_tickets} студентов 👨🏻‍🎓
""".strip()

LOTTERY_INFO_TEXT = """
Чтобы поучаствовать в лотерее, нужно получить лотерейный билет. Для этого ищи точку в местах празднования:

<b>Проспект Вернадского, 78</b> — в холле корпуса А, около штанов.
<b>Проспект Вернадского, 86</b> —  в чилл-аут зоне.
<b>Улица Стромынка, 20 </b>— в чилл-аут зоне, около 401 аудитории.

🔗 <b>Итоги онлайн-лотереи будут подводиться на трансляции 28 января в 18:30</b> <b>в паблике </b><a href="http://vk.com/sumirea"><b>Студенческого союза МИРЭА</b></a>
""".strip()  # noqa: E501

LOTTERY_TICKET_TEXT = """
Ты тоже участвуешь! Твой билет <b>№{ticket_id}</b>
""".strip()


lottery_info_window = Window(
    Format(LOTTERY_USERS_TEXT + "\n"),
    Const(LOTTERY_INFO_TEXT + "\n"),
    Format(LOTTERY_TICKET_TEXT, when=F["ticket_id"].is_not(None)),
    GoToMenuButton(),
    getter=get_lottery_info,
    state=ViewLotteryStates.view,
)

lottery_dialog = Dialog(lottery_info_window)
