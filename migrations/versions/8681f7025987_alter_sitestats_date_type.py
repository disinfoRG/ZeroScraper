"""alter sitestats date type

Revision ID: 8681f7025987
Revises: ff3952ed9955
Create Date: 2020-04-14 13:13:08.400087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8681f7025987'
down_revision = 'ff3952ed9955'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "SiteStats", "date", type_=sa.Date, nullable=False
    )


def downgrade():
    op.alter_column(
        "SiteStats", "date", type_=sa.String(32), nullable=False
    )