"""drop url hash unique constraint

Revision ID: 1e590240b89f
Revises: 532fa603f39a
Create Date: 2020-01-10 14:03:10.118443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1e590240b89f"
down_revision = "532fa603f39a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ik_Article_url_hash", "Article", ["url_hash"])
    op.drop_constraint("uq_Article_url_hash", "Article", type_="unique")


def downgrade():
    op.create_unique_constraint("uq_Article_url_hash", "Article", ["url_hash"])
    op.drop_index("ik_Article_url_hash", "Article")
