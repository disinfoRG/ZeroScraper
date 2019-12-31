"""add info columns

Revision ID: 95e1de28f5ba
Revises: bed50d892f5a
Create Date: 2019-12-31 16:19:07.623361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "95e1de28f5ba"
down_revision = "bed50d892f5a"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("FBPostSnapshot", "fb_post_id")
    op.drop_column("FBCommentSnapshot", "fb_comment_id")
    op.add_column("Site", sa.Column("site_info", sa.JSON, nullable=False))
    op.add_column("FBPostSnapshot", sa.Column("fb_post_info", sa.JSON, nullable=False))
    op.add_column("FBPostSnapshot", sa.Column("author_info", sa.JSON, nullable=False))
    op.add_column(
        "FBCommentSnapshot", sa.Column("fb_comment_info", sa.JSON, nullable=False)
    )
    op.add_column(
        "FBCommentSnapshot", sa.Column("author_info", sa.JSON, nullable=False)
    )


def downgrade():
    op.drop_column("Site", "site_info")
    op.drop_column("FBPostSnapshot", "fb_post_info")
    op.drop_column("FBPostSnapshot", "author_info")
    op.drop_column("FBCommentSnapshot", "fb_comment_info")
    op.drop_column("FBCommentSnapshot", "author_info")
    op.add_column("FBCommentSnapshot", sa.Column("fb_comment_id", sa.String(255)))
    op.add_column("FBPostSnapshot", sa.Column("fb_post_id", sa.String(255)))
