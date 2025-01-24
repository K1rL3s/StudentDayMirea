from io import BytesIO
from typing import Any

from qrcode.constants import ERROR_CORRECT_L
from qrcode.image.pure import PyPNGImage
from qrcode.main import QRCode

from core.ids import ProductId, QuestId, TaskId, UserId

UserIdPrefix = "id_"
TaskIdPrefix = "task_"
QuestIdPrefix = "quest_"
ProductIdPrefix = "product_"


class QRCodeService:
    def __init__(self, bot_name: str) -> None:
        self.bot_name = bot_name
        self.qr = QRCode(
            version=None,
            error_correction=ERROR_CORRECT_L,
            box_size=8,
            border=4,
            image_factory=PyPNGImage,
        )

    def user_qrcode(self, user_id: UserId) -> BytesIO:
        return self._generate_qrcode(UserIdPrefix, user_id)

    def task_qrcode(self, task_id: TaskId) -> BytesIO:
        return self._generate_qrcode(TaskIdPrefix, task_id)

    def product_qrcode(self, product_id: ProductId) -> BytesIO:
        return self._generate_qrcode(ProductIdPrefix, product_id)

    def quest_qrcode(self, quest_id: QuestId) -> BytesIO:
        return self._generate_qrcode(QuestIdPrefix, quest_id)

    def task_deeplink(self, task_id: TaskId) -> str:
        return self._generate_deeplink(TaskIdPrefix, task_id)

    def _generate_qrcode(self, prefix: str, data: Any) -> BytesIO:
        self.qr.clear()

        deeplink = self._generate_deeplink(prefix, data)
        self.qr.add_data(deeplink)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color="black", back_color="white")

        self.qr.clear()

        stream = BytesIO()
        img.save(stream=stream)

        return stream

    def _generate_deeplink(self, prefix: str, data: Any) -> str:
        return f"https://t.me/{self.bot_name}?start={prefix}{data}"


if __name__ == "__main__":
    generator = QRCodeService("pandito_bot")
    with open("test.png", "wb") as f:
        image = generator.user_qrcode(UserId(2015866626))
        f.write(image.getvalue())
