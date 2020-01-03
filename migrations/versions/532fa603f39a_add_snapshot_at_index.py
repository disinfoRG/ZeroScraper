"""add snapshot_at index

Revision ID: 532fa603f39a
Revises: 2f07cdaab83d
Create Date: 2020-01-03 18:14:48.681396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "532fa603f39a"
down_revision = "2f07cdaab83d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "idx_ArticleSnapshot_snapshot_at", "ArticleSnapshot", ["snapshot_at"]
    )


def downgrade():
    op.drop_index("idx_ArticleSnapshot_snapshot_at", "ArticleSnapshot")
