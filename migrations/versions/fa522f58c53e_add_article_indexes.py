"""add article indexes

Revision ID: fa522f58c53e
Revises: 4d0b16c54ce0
Create Date: 2020-03-17 21:19:45.448623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fa522f58c53e"
down_revision = "4d0b16c54ce0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "ik_Article_site_id_next_snapshot_at",
        "Article",
        ["site_id", "next_snapshot_at"],
    )
    op.create_index(
        "ik_Article_site_id_last_snapshot_at",
        "Article",
        ["site_id", "last_snapshot_at"],
    )
    op.create_index(
        "ik_Article_site_id_first_snapshot_at",
        "Article",
        ["site_id", "first_snapshot_at"],
    )


def downgrade():
    op.drop_index("ik_Article_site_id_first_snapshot_at", "Article")
    op.drop_index("ik_Article_site_id_last_snapshot_at", "Article")
    op.drop_index("ik_Article_site_id_next_snapshot_at", "Article")
