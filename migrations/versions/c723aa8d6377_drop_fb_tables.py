"""drop fb tables

Revision ID: c723aa8d6377
Revises: a0a180e48e88
Create Date: 2020-03-09 16:22:48.889314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c723aa8d6377"
down_revision = "a0a180e48e88"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("FBCommentSnapshot")
    op.drop_table("FBPostSnapshot")


def downgrade():
    op.create_table(
        "FBPostSnapshot",
        sa.Column("article_id", sa.Integer, nullable=False),
        sa.Column("snapshot_at", sa.Integer, nullable=False),
        sa.Column("raw_data", sa.dialects.mysql.MEDIUMTEXT),
        sa.Column("author", sa.String(1024)),
        sa.Column("shared_url", sa.String(1024)),
        sa.Column("reactions", sa.JSON),
        sa.Column("fb_post_info", sa.JSON, nullable=False),
        sa.Column("author_info", sa.JSON, nullable=False),
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
        sa.Column("fb_comment_info", sa.JSON, nullable=False),
        sa.Column("author_info", sa.JSON, nullable=False),
        sa.PrimaryKeyConstraint(
            "article_id", "snapshot_at", name="pk_FBCommentSnapshot"
        ),
    )
