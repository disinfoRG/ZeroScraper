"""add stats table

Revision ID: 4d0b16c54ce0
Revises: c723aa8d6377
Create Date: 2020-03-15 18:09:25.705669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d0b16c54ce0'
down_revision = 'c723aa8d6377'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "SiteStats",
        sa.Column("site_id", sa.Integer, nullable=False),
        sa.Column("date", sa.String(32), nullable=False),
        sa.Column("new_posts_count", sa.Integer),
        sa.Column("revisit_posts_count", sa.Integer),
        sa.PrimaryKeyConstraint("site_id", "date", name="pk_SiteStats"),
    )


def downgrade():
    op.drop_table("SiteStats")
