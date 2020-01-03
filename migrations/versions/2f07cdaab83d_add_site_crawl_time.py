"""add Site crawl time

Revision ID: 2f07cdaab83d
Revises: 57f2f8bca25a
Create Date: 2020-01-03 16:36:15.017188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2f07cdaab83d"
down_revision = "57f2f8bca25a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("Site", sa.Column("last_crawl_at", sa.Integer))


def downgrade():
    op.drop_column("Site", "last_crawl_at")
