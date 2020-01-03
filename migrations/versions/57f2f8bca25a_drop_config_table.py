"""drop config table

Revision ID: 57f2f8bca25a
Revises: 95e1de28f5ba
Create Date: 2019-12-14 11:07:07.479154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "57f2f8bca25a"
down_revision = "95e1de28f5ba"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("Config")


def downgrade():
    op.create_table(
        "Config",
        sa.Column("key", sa.String(128), nullable=False),
        sa.Column("type", sa.String(128), nullable=False),
        sa.Column("value", sa.String(128), nullable=False),
    )
