"""add redirect to hash

Revision ID: 360d0f705ee3
Revises: 8681f7025987
Create Date: 2020-05-15 00:53:38.230645

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import BINARY


# revision identifiers, used by Alembic.
revision = "360d0f705ee3"
down_revision = "8681f7025987"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("Article", sa.Column("redirect_to_hash", BINARY(16)))
    op.execute("UPDATE Article SET redirect_to_hash = UNHEX(MD5(redirect_to))")
    op.create_index("ik_Article_redirect_to_hash", "Article", ["redirect_to_hash"])


def downgrade():
    op.drop_index("ik_Article_redirect_to_hash", "Article")
    op.drop_column("Article", "redirect_to_hash")
