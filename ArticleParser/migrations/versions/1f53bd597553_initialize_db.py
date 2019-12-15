"""initialize db

Revision ID: 1f53bd597553
Revises:
Create Date: 2019-12-15 09:41:26.041988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1f53bd597553"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "producer",
        sa.Column("producer_id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text),
        sa.Column("classification", sa.String(256)),
        sa.Column("canonical_url", sa.String(1024)),
        sa.Column("languages", sa.JSON),
        sa.Column("licenses", sa.JSON),
        sa.Column("first_seen_at", sa.Integer),
        sa.Column("last_updated_at", sa.Integer),
        sa.Column("followership", sa.JSON),
    )
    op.create_table(
        "publication",
        sa.Column("publication_id", sa.Integer, primary_key=True),
        sa.Column("producer_id", sa.Integer),
        sa.Column("canonical_url", sa.String(1024)),
        sa.Column("title", sa.Text),
        sa.Column("publication_text", sa.Text),
        sa.Column("language", sa.String(256)),
        sa.Column("license", sa.String(256)),
        sa.Column("posted_at", sa.Integer),
        sa.Column("first_seen_at", sa.Integer),
        sa.Column("last_updated_at", sa.Integer),
        sa.Column("hashtags", sa.JSON),
        sa.Column("urls", sa.JSON),
        sa.Column("keywords", sa.JSON),
        sa.Column("tags", sa.JSON),
    )


def downgrade():
    op.drop_table("publication")
    op.drop_table("producer")
