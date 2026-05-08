"""Merge migration heads

Revision ID: 82eda4213fdb
Revises: 839a3d19722c, fc42558dbb4b
Create Date: 2026-05-07 21:27:15.222265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82eda4213fdb'
down_revision = ('839a3d19722c', 'fc42558dbb4b')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
