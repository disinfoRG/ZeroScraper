"""refactor site json to config

Revision ID: 3fb234ff2fb5
Revises: da6f10c8ebf4
Create Date: 2019-12-03 11:18:46.478703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3fb234ff2fb5"
down_revision = "da6f10c8ebf4"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE Site SET config = '{}' WHERE config = ''")
    op.alter_column(
        "Site", "config", type_=sa.JSON, existing_type=sa.Text, nullable=False
    )


def downgrade():
    op.alter_column(
        "Site", "config", type_=sa.Text, existing_type=sa.JSON, nullable=False
    )
    op.execute("UPDATE Site SET config = '' WHERE config = '{}'")
