"""add rating column to responses

Revision ID: b66353501748
Revises: 97c4d19f7621
Create Date: 2025-05-12 14:06:32.005260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b66353501748'
down_revision: Union[str, None] = '97c4d19f7621'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('responses', sa.Column('rating', sa.Integer(), sa.CheckConstraint('rating >= 0 AND rating <= 5'), nullable=True))


def downgrade() -> None:
    op.drop_column('responses', 'rating')
