"""qrcode

Revision ID: 0006
Revises: 0005
Create Date: 2024-12-12 21:52:19.826979

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("qrcode_image_id", sa.String(length=128), nullable=True),
    )
    op.create_unique_constraint(
        op.f("uq_users_qrcode_image_id"),
        "users",
        ["qrcode_image_id"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq_users_qrcode_image_id"), "users", type_="unique")
    op.drop_column("users", "qrcode_image_id")
    # ### end Alembic commands ###
