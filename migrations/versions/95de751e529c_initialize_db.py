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
        "Article",
        sa.Column("article_id", sa.Integer, primary_key=True),
        sa.Column("url", sa.String(255)),
    )

    op.create_table(
        "ArticleSnapshot",
        sa.Column("article_id", sa.Integer, sa.ForeignKey("Article.article_id")),
        sa.Column("raw_body", sa.Text),
    )


def downgrade():
    op.drop_table("ArticleSnapshot")
    op.drop_table("Article")
