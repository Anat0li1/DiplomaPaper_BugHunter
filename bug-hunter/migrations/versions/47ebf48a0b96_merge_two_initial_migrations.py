"""Merge two initial migrations

Revision ID: 47ebf48a0b96
Revises: 20260503_0001, 2b89398bc0bf
Create Date: 2026-05-06 11:09:07.343776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47ebf48a0b96'
down_revision = ('20260503_0001', '2b89398bc0bf')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

