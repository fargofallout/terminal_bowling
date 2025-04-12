"""add head-to-head columns

Revision ID: 2174fcabe2b5
Revises: 951e9d7c828c
Create Date: 2025-02-18 02:30:17.995992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2174fcabe2b5'
down_revision: Union[str, None] = '951e9d7c828c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("head_to_head_game_table", sa.Column("game_number", sa.Integer))
    op.add_column("bowler_head_to_head_game_table", sa.Column("head_to_head_game_id", sa.Integer, sa.ForeignKey("head_to_head_game_table.id")))


def downgrade() -> None:
    op.drop_column("head_to_head_game_table", "game_number")
    op.drop_column("bowler_head_to_head_game_table", "head_to_head_game_id")
