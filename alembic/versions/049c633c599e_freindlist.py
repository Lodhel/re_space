"""freindlist

Revision ID: 049c633c599e
Revises: 2189dfd9a493
Create Date: 2020-11-21 21:21:37.891601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '049c633c599e'
down_revision = '2189dfd9a493'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'friend_list',
        sa.Column("id", sa.Integer(), primary_key=True, unique=True),
        sa.Column('user', sa.Integer()),
        sa.Column('array', sa.Text())
    )


def downgrade():
    pass
