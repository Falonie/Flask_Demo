"""drop_null

Revision ID: e183b08e9710
Revises: 5a4b580dc007
Create Date: 2018-06-06 21:10:01.373000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e183b08e9710'
down_revision = '5a4b580dc007'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_hash',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('user', 'telephone',
               existing_type=mysql.VARCHAR(length=11),
               nullable=True)
    op.alter_column('user', 'username',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'username',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('user', 'telephone',
               existing_type=mysql.VARCHAR(length=11),
               nullable=False)
    op.alter_column('user', 'password_hash',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###