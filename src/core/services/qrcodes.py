from io import BytesIO
from typing import Any

from qrcode.constants import ERROR_CORRECT_L
from qrcode.image.pure import PyPNGImage
from qrcode.main import QRCode

from core.ids import TaskId, UserId

_UserIdPrefix = "id_"
_TaskIdPrefix = "task_"


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

    def user_id_qrcode(self, user_id: UserId) -> BytesIO:
        return self._generate_qrcode(_UserIdPrefix, user_id)

    def task_id_qrcode(self, task_id: TaskId) -> BytesIO:
        return self._generate_qrcode(_TaskIdPrefix, task_id)

    def _generate_qrcode(self, prefix: str, data: Any) -> BytesIO:
        self.qr.clear()

        deeplink = f"https://t.me/{self.bot_name}?start={prefix}{data}"
        self.qr.add_data(deeplink)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color="black", back_color="white")

        self.qr.clear()

        stream = BytesIO()
        img.save(stream=stream)

        return stream


if __name__ == "__main__":
    generator = QRCodeService("pandito_bot")
    with open("test.png", "wb") as f:
        image = generator.user_id_qrcode(2015866626)
        f.write(image.getvalue())
