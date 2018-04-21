"""initial migration

Revision ID: 322435acfc3c
Revises: 7ba43bde60a6
Create Date: 2018-04-18 17:47:12.083000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '322435acfc3c'
down_revision = '7ba43bde60a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=100), nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', mysql.VARCHAR(length=100), nullable=False))
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###
