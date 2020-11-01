"""user table

Revision ID: 2f1a954324c9
Revises: 
Create Date: 2020-11-01 20:19:13.047093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f1a954324c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'base_user',
        sa.Column("id", sa.Integer(), primary_key=True, unique=True),
        sa.Column('login', sa.String(50)),
        sa.Column('password', sa.Text(())),
        sa.Column('token', sa.Text())
    )

    op.create_table(
        'profile',
        sa.Column('id', sa.Integer, primary_key=True, unique=True),
        sa.Column('user', sa.Integer, unique=True),
        sa.Column('first_name', sa.String(50)),
        sa.Column('date_join', sa.Date, nullable=True),
        sa.Column('phone', sa.String(32)),
        sa.Column('date_birthday', sa.Date, nullable=True),
        sa.Column('gender', sa.String(8))
    )

def downgrade():
    pass
