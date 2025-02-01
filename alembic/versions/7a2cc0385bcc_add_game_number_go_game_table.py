"""add game number go game table

Revision ID: 7a2cc0385bcc
Revises: 9dc977809cc8
Create Date: 2025-02-01 13:47:39.100682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a2cc0385bcc'
down_revision: Union[str, None] = '9dc977809cc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("game_table", sa.Column("game_number", sa.Integer, nullable=True))


def downgrade() -> None:
    pass
