"""add snapshot_at_date

Revision ID: ff3952ed9955
Revises: 53e9ac7f3eb8
Create Date: 2020-03-31 21:06:04.358177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ff3952ed9955"
down_revision = "53e9ac7f3eb8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("ArticleSnapshot", sa.Column("snapshot_at_date", sa.DateTime))
    op.execute(
        "UPDATE ArticleSnapshot SET snapshot_at_date = FROM_UNIXTIME(snapshot_at)"
    )
    op.alter_column(
        "ArticleSnapshot", "snapshot_at_date", existing_type=sa.DateTime, nullable=False
    )
    op.execute(
        "ALTER TABLE ArticleSnapshot DROP PRIMARY KEY, ADD PRIMARY KEY (article_id, snapshot_at, snapshot_at_date)"
    )


def downgrade():
    op.execute(
        "ALTER TABLE ArticleSnapshot DROP PRIMARY KEY, ADD PRIMARY KEY (article_id, snapshot_at)"
    )
    op.drop_column("ArticleSnapshot", "snapshot_at_date")
