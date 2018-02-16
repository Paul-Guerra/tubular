"""add date column to crawl table

Revision ID: e93f517ea028
Revises: 0a52e2dc9f79
Create Date: 2018-02-15 23:17:45.394477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e93f517ea028'
down_revision = '0a52e2dc9f79'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('crawl',
        sa.Column('updated', sa.DATETIME, server_default=sa.func.now())
    )


def downgrade():
    op.drop_column('crawl', 'updated')
