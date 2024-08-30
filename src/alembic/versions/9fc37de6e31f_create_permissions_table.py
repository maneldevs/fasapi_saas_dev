"""create permissions table

Revision ID: 9fc37de6e31f
Revises: d4986fb5c6ff
Create Date: 2024-08-30 12:08:08.090201

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "9fc37de6e31f"
down_revision: Union[str, None] = "d4986fb5c6ff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "permissions",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("scope", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("scope_owner", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("role_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("resource_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(["resource_id"], ["resources.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("role_id", "resource_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("permissions")
    # ### end Alembic commands ###
