"""empty message

Revision ID: 16d6afe18d85
Revises: 954f0be5cab3
Create Date: 2022-05-09 19:51:51.128771

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '16d6afe18d85'
down_revision = '954f0be5cab3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tests', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.alter_column('tests', 'creator_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tests', 'creator_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('tests', 'created_on')
    # ### end Alembic commands ###
