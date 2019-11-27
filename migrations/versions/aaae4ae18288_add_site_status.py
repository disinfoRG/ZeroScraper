"""add_site_status

Revision ID: aaae4ae18288
Revises: 95de751e529c
Create Date: 2019-11-27 11:55:07.162409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aaae4ae18288"
down_revision = "95de751e529c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("Site", sa.Column("is_active", sa.Boolean, default=False))


def downgrade():
    op.drop_column("Site", "is_active")
