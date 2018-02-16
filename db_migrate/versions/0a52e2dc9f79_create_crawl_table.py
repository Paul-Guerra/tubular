"""create crawl table

Revision ID: 0a52e2dc9f79
Revises: 
Create Date: 2018-02-15 22:56:18.265772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a52e2dc9f79'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'crawl',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('url', sa.VARCHAR(2000), nullable=False),
        sa.Column('content', sa.TEXT)
    )

def downgrade():
    op.drop_table("crawl")
