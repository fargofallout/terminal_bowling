"""add game table

Revision ID: 1dca93bb8f54
Revises: 9764151565b6
Create Date: 2024-12-15 11:01:44.926763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dca93bb8f54'
down_revision: Union[str, None] = '9764151565b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("game_table", 
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("score", sa.Integer),
        sa.Column("handicap", sa.Integer),
        sa.Column("game_number", sa.Integer),
        sa.Column("bowler_id", sa.Integer, sa.ForeignKey("bowler_table.id")),
    )



def downgrade() -> None:
    op.drop_table("game_table")
