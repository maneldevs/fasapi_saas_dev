"""create modules and groups_modules

Revision ID: d63087471e46
Revises: 54ca22122ec8
Create Date: 2024-08-27 07:22:50.820272

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "d63087471e46"
down_revision: Union[str, None] = "54ca22122ec8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "modules",
        sa.Column("code", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("webname", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "group_module",
        sa.Column("group_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("module_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
        ),
        sa.ForeignKeyConstraint(
            ["module_id"],
            ["modules.id"],
        ),
        sa.PrimaryKeyConstraint("group_id", "module_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("group_module")
    op.drop_table("modules")
    # ### end Alembic commands ###