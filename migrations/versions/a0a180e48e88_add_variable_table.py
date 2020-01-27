"""add variable table

Revision ID: a0a180e48e88
Revises: 6924196dcf9f
Create Date: 2020-01-27 15:15:48.713506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a0a180e48e88"
down_revision = "6924196dcf9f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "Variable",
        sa.Column("key", sa.String(128), nullable=False, primary_key=True),
        sa.Column("value", sa.String(128), nullable=False),
    )


def downgrade():
    op.drop_table("Variable")
