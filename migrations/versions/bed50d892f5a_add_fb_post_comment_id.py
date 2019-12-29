"""add fb post comment id

Revision ID: bed50d892f5a
Revises: 6a9f69af5ba7
Create Date: 2019-12-28 17:01:29.618961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bed50d892f5a"
down_revision = "6a9f69af5ba7"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("FBPostSnapshot", sa.Column("fb_post_id", sa.String(255)))
    op.add_column("FBCommentSnapshot", sa.Column("fb_comment_id", sa.String(255)))


def downgrade():
    op.drop_column("FBPostSnapshot", "fb_post_id")
    op.drop_column("FBCommentSnapshot", "fb_comment_id")
