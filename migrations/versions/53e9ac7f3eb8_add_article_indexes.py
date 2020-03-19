"""add article indexes

Revision ID: 53e9ac7f3eb8
Revises: fa522f58c53e
Create Date: 2020-03-18 18:41:49.708505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "53e9ac7f3eb8"
down_revision = "fa522f58c53e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "ik_Article_site_id_article_id", "Article", ["site_id", "article_id"]
    )


def downgrade():
    op.drop_index("ik_Article_site_id_article_id", table_name="Article")
