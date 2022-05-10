"""add in tests table forgein key

Revision ID: 52826a1b7e30
Revises: c86e92961432
Create Date: 2022-03-31 19:57:28.476362

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '52826a1b7e30'
down_revision = 'c86e92961432'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tests', sa.Column('creator', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key(None, 'tests', 'users', ['creator'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tests', type_='foreignkey')
    op.drop_column('tests', 'creator')
    # ### end Alembic commands ###
