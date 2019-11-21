"""initialize db

Revision ID: 95de751e529c
Revises:
Create Date: 2019-11-13 07:50:11.050035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "95de751e529c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "Config",
        sa.Column("key", sa.String(128), nullable=False),
        sa.Column("type", sa.String(128), nullable=False),
        sa.Column("value", sa.String(128), nullable=False),
    )
    op.create_table(
        "Site",
        sa.Column("site_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("type", sa.String(128), nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("url", sa.String(1024), nullable=False),
        sa.Column("config", sa.Text, nullable=False),
    )
    op.create_table(
        "Article",
        sa.Column("article_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("site_id", sa.Integer, nullable=False),
        sa.Column("url", sa.String(1024), nullable=False),
        sa.Column("url_hash", sa.String(32), nullable=False),
        sa.Column("first_snapshot_at", sa.Integer, nullable=False),
        sa.Column("last_snapshot_at", sa.Integer, nullable=False),
        sa.Column("next_snapshot_at", sa.Integer, nullable=False),
        sa.Column("snapshot_count", sa.Integer, nullable=False),
        sa.Column("redirect_to", sa.String(1024)),
        sa.UniqueConstraint("url_hash", name="uq_Article_url_hash"),
    )
    op.create_table(
        "ArticleSnapshot",
        sa.Column("article_id", sa.Integer, nullable=False),
        sa.Column("snapshot_at", sa.Integer, nullable=False),
        sa.Column("raw_data", sa.dialects.mysql.MEDIUMTEXT),
        sa.PrimaryKeyConstraint("article_id", "snapshot_at", name="pk_ArticleSnapshot"),
    )


def downgrade():
    op.drop_table("ArticleSnapshot")
    op.drop_table("Article")
    op.drop_table("Site")
    op.drop_table("Config")
