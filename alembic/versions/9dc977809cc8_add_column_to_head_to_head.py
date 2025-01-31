"""add column to head to head

Revision ID: 9dc977809cc8
Revises: 4be94e54081b
Create Date: 2025-01-31 14:04:01.440904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dc977809cc8'
down_revision: Union[str, None] = '4be94e54081b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("head_to_head_table", sa.Column("week_number", sa.Integer))
    op.add_column("head_to_head_table", sa.Column("week_complete", sa.Boolean))


def downgrade() -> None:
    pass
