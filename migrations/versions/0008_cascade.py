"""cascade

Revision ID: 0008
Revises: 0007
Create Date: 2025-01-24 19:56:30.098816

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0008"
down_revision: str | None = "0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "fk_lottery_tickets_user_id_users",
        "lottery_tickets",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_lottery_tickets_user_id_users"),
        "lottery_tickets",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_lottery_tickets_user_id_users"),
        "lottery_tickets",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_lottery_tickets_user_id_users",
        "lottery_tickets",
        "users",
        ["user_id"],
        ["id"],
    )
    # ### end Alembic commands ###
