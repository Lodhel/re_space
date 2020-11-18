"""food

Revision ID: 2189dfd9a493
Revises: 312eac954ac0
Create Date: 2020-11-18 20:51:45.595703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2189dfd9a493'
down_revision = '312eac954ac0'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'food',
        sa.Column("id", sa.Integer(), primary_key=True, unique=True),
        sa.Column("item", sa.Integer()),
        sa.Column("user", sa.Integer()),
        sa.Column('status', sa.String(16)),
        sa.Column('amount', sa.String(16)),
        sa.Column('measure', sa.String(16)),
        sa.Column('date_start', sa.Date, nullable=True),
        sa.Column('date_end', sa.Date, nullable=True)
    )


def downgrade():
    pass
