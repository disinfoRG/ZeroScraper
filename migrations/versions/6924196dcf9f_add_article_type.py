"""add article type

Revision ID: 6924196dcf9f
Revises: 1e590240b89f
Create Date: 2020-01-14 12:28:55.741356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6924196dcf9f"
down_revision = "1e590240b89f"
branch_labels = None
depends_on = None


def upgrade():
    article_type = sa.dialects.mysql.ENUM(
        "Article", "FBPost", "FBComment", "PTT", "Dcard"
    )
    op.alter_column(
        "Article", "article_type", nullable=False, existing_type=article_type
    )


def downgrade():
    article_type = sa.dialects.mysql.ENUM("Article", "FBPost", "FBComment")
    op.alter_column(
        "Article", "article_type", nullable=False, existing_type=article_type
    )
