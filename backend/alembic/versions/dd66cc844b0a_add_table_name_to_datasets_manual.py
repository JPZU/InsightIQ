"""Add table_name to datasets (manual)

Revision ID: dd66cc844b0a
Revises: 97c4d19f7621
Create Date: 2025-05-14 11:33:26.666834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd66cc844b0a'
down_revision: Union[str, None] = '97c4d19f7621'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('datasets', sa.Column('table_name', sa.String(length=255), nullable=False, server_default='default_table'))
    op.alter_column('datasets', 'table_name', server_default=None)


def downgrade() -> None:
    op.drop_column('datasets', 'table_name')