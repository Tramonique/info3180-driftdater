"""Add seen field to matches

Revision ID: 904f52a50c3e
Revises: 82eda4213fdb
Create Date: 2026-05-07 22:08:22.662242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '904f52a50c3e'
down_revision = '82eda4213fdb'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('matches', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seen', sa.Boolean(), nullable=False, server_default='false'))


def downgrade():
    with op.batch_alter_table('matches', schema=None) as batch_op:
        batch_op.drop_column('seen')