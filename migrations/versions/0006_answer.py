"""answer

Revision ID: 0006
Revises: 0005
Create Date: 2025-01-24 17:38:43.979958

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
        "quests",
        sa.Column("wrong_answer", sa.String(length=128), nullable=False),
    )
    op.add_column(
        "quests",
        sa.Column("right_answer", sa.String(length=128), nullable=False),
    )
    op.alter_column(
        "quests",
        "title",
        existing_type=sa.VARCHAR(length=256),
        type_=sa.String(length=64),
        existing_nullable=False,
    )
    op.alter_column(
        "quests",
        "answer",
        existing_type=sa.VARCHAR(length=256),
        type_=sa.String(length=128),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "quests",
        "answer",
        existing_type=sa.String(length=128),
        type_=sa.VARCHAR(length=256),
        existing_nullable=False,
    )
    op.alter_column(
        "quests",
        "title",
        existing_type=sa.String(length=64),
        type_=sa.VARCHAR(length=256),
        existing_nullable=False,
    )
    op.drop_column("quests", "right_answer")
    op.drop_column("quests", "wrong_answer")
    # ### end Alembic commands ###
