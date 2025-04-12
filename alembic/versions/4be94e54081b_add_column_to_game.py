"""add column to game

Revision ID: 4be94e54081b
Revises: 6b2ccb2edc3e
Create Date: 2025-01-31 14:01:45.536536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4be94e54081b'
down_revision: Union[str, None] = '6b2ccb2edc3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("game_table", sa.Column("is_robot_game", sa.Boolean, nullable=True))


def downgrade() -> None:
    op.drop_column("game_table", "is_robot_game")
