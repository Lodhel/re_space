"""Items objects

Revision ID: 312eac954ac0
Revises: 2f1a954324c9
Create Date: 2020-11-08 20:19:30.638507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '312eac954ac0'
down_revision = '2f1a954324c9'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'category_item',
        sa.Column("id", sa.Integer(), primary_key=True, unique=True),
        sa.Column('title', sa.String(50))
    )

    op.create_table(
        'location',
        sa.Column("id", sa.Integer(), primary_key=True, unique=True),
        sa.Column('title', sa.String(50)),
        sa.Column('article', sa.Text(()))
    )

    op.create_table(
        'item',
        sa.Column("id", sa.Integer(), primary_key=True, unique=True),
        sa.Column("location", sa.Integer()),
        sa.Column("category", sa.Integer()),
        sa.Column('title', sa.String(50)),
        sa.Column('article', sa.Text(())),
        sa.Column('attribute', sa.Text())
    )





def downgrade():
    pass
