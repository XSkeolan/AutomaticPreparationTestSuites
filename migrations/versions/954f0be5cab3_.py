"""empty message

Revision ID: 954f0be5cab3
Revises: 28d498193f6f
Create Date: 2022-05-08 00:55:28.097959

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '954f0be5cab3'
down_revision = '28d498193f6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tests_creator_fkey', 'tests', type_='foreignkey')
    op.create_foreign_key(None, 'tests', 'users', ['creator_id'], ['id'])
    # ### end Alembic commands ###