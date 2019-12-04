"""add facebook tables

Revision ID: 6a9f69af5ba7
Revises: da6f10c8ebf4
Create Date: 2019-12-04 11:12:24.182307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6a9f69af5ba7"
down_revision = "3fb234ff2fb5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "FBPostSnapshot",
        sa.Column("article_id", sa.Integer, nullable=False),
        sa.Column("snapshot_at", sa.Integer, nullable=False),
        sa.Column("raw_data", sa.dialects.mysql.MEDIUMTEXT),
        sa.Column("author", sa.String(1024)),
        sa.Column("shared_url", sa.String(1024)),
        sa.Column("reactions", sa.JSON),
        sa.PrimaryKeyConstraint("article_id", "snapshot_at", name="pk_FBPostSnapshot"),
    )
    op.create_table(
        "FBCommentSnapshot",
        sa.Column("article_id", sa.Integer, nullable=False),
        sa.Column("snapshot_at", sa.Integer, nullable=False),
        sa.Column("raw_data", sa.dialects.mysql.MEDIUMTEXT),
        sa.Column("author", sa.String(1024)),
        sa.Column("reply_to", sa.Integer, nullable=False),
        sa.Column("reactions", sa.JSON),
        sa.PrimaryKeyConstraint(
            "article_id", "snapshot_at", name="pk_FBCommentSnapshot"
        ),
    )

    article_type = sa.dialects.mysql.ENUM("Article", "FBPost", "FBComment")
    op.add_column("Article", sa.Column("article_type", article_type))
    op.execute("UPDATE Article SET article_type = 'Article' WHERE article_type IS NULL")
    op.alter_column(
        "Article", "article_type", nullable=False, existing_type=article_type
    )


def downgrade():
    op.drop_column("Article", "article_type")
    op.drop_table("FBCommentSnapshot")
    op.drop_table("FBPostSnapshot")
