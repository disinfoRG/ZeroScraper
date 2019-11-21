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
        "Site",
        sa.Column("site_id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text),
        sa.Column("type", sa.String(128)),
    )
    op.create_table(
        "SiteEntry",
        sa.Column("site_id", sa.BigInteger, sa.ForeignKey("Site.site_id")),
        sa.Column("url", sa.String(512)),
        sa.PrimaryKeyConstraint("site_id", "url", name="pk_SiteEntry"),
    )
    op.create_table(
        "SiteArticleURLMatch",
        sa.Column(
            "site_id", sa.BigInteger, sa.ForeignKey("Site.site_id"), primary_key=True
        ),
        sa.Column("article_url_match", sa.String(512)),
        sa.Column("snapshot_freq", sa.String(128)),
        sa.Column("parser_id", sa.Integer),
    )
    op.create_table(
        "Article",
        sa.Column("article_id", sa.BigInteger, primary_key=True),
        sa.Column("site_id", sa.BigInteger, sa.ForeignKey("Site.site_id")),
        sa.Column("url", sa.String(1024)),
        sa.Column("url_hash", sa.String(512)),
        sa.Column("first_snapshot_at", sa.Integer),
        sa.Column("last_snapshot_at", sa.Integer),
        sa.Column("next_snapshot_at", sa.Integer),
        sa.Column("snapshot_count", sa.BigInteger),
        sa.Column("redirect_to", sa.String(1024)),
    )
    op.create_index("ik_Article_url_hash", "Article", ["url_hash"])
    op.create_index("ik_Article_next_snapshot_at", "Article", ["next_snapshot_at"])
    op.create_index(
        "ik_Article_site_id_first_snapshot_at",
        "Article",
        ["site_id", "first_snapshot_at"],
    )

    op.create_table(
        "ArticleSnapshot",
        sa.Column("article_id", sa.BigInteger, sa.ForeignKey("Article.article_id")),
        sa.Column("snapshot_at", sa.Integer),
        sa.Column("raw_body", sa.Text),
        sa.PrimaryKeyConstraint("article_id", "snapshot_at", name="pk_ArticleSnapshot"),
    )


def downgrade():
    op.drop_table("ArticleSnapshot")
    op.drop_table("Article")
    op.drop_table("SiteArticleURLMatch")
    op.drop_table("SiteEntry")
    op.drop_table("Site")
