"""Add new foreign key to Game table

Revision ID: 1e6ff62c1f59
Revises: 2174fcabe2b5
Create Date: 2025-03-08 15:58:06.260113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e6ff62c1f59'
down_revision: Union[str, None] = '2174fcabe2b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("game_table", sa.Column("bowler_head_to_head_game_id", sa.Integer, sa.ForeignKey("bowler_head_to_head_game_table.id")))


def downgrade() -> None:
    op.drop_column("game_table", "bowler_head_to_head_game_id")
